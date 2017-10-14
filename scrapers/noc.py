import re
import logging

import requests
from bs4 import BeautifulSoup

from template import *

BASE_URL = 'http://noc.esdc.gc.ca/English/noc'
SEARCH_URL = '%s/QuickSearch.aspx' % BASE_URL
POSTING_URL = '%s/ProfileQuickSearch.aspx' % BASE_URL

DATA_FILE = "../data/positions.csv"
JOBS_FILE = "../data/job_names.csv"

all_requirements_pat = r'Employment requirements</h3>(.*?)<h3>'
li_pat = r'<li>(.*?)</li>'

def _seperate_requirements(strData):
    # string -> list
    return re.findall(li_pat, strData)


def jobDetails(query):
    # string -> list
    # Job Details can take a 4 digit code
    # or the entire link
    data = str(requests.get(
        POSTING_URL,
        params = {'val1': query} if len(query) == 4 else None
    ).content)
    allRequirements = re.findall(all_requirements_pat, data)
    if len(allRequirements) > 0:
        return _seperate_requirements(allRequirements[0])
    else:
        return None


def _scrape_item(data):
    # BeautifulSoup -> dictionary
    urlBox = data.find('a')
    if urlBox is not None:
        return {
            'link': '%s%s' % (BASE_URL, urlBox.href,),
            'title': urlBox.text[5:],
            'requirements': jobDetails(urlBox.text[:4]),
        }

def _seperate_list(data):
    # BeautifulSoup -> list
    results = data.find('ul', {'class': 'NoBulletList  NoIndent'})
    result = [_scrape_item(x) for x in results]

def search(query):
    # string -> dictionary
    data = BeautifulSoup(
        requests.get(
            SEARCH_URL,
            params = {'val65': query},
        ).content,
        'html.parser',
    )

    positionsData = data.find(
        'ul', {'class': 'NoBulletList NoIndent'}
    )
    if positionsData is not None:
        return _scrape_item(
            positionsData.findAll(
                'li', {'class': ''}
            )[-1]
        )
    else:
        return None

def giantSearch(allJobs):
    # Saves results of each right after scraping
    unfoundJobs = []
    with open(DATA_FILE, 'w+') as csv:
        for job in allJobs:
            logging.debug("Searching for data on %s" % (job,))
            data = search(job)
            if data is not None:
                row = '%s,%s\n' % (data['title'], ','.join(data['requirements']))
                csv.write(row)
            else:
                unfoundJobs.append(job)
        logging.critical('There were %i unfound jobs of' % (len(unfoundJobs)))
        logging.critical(unfoundJobs)

def smartDownload():
    page = BeautifulSoup(
        requests.get(
            'http://www.cic.gc.ca/english/immigrate/skilled/noc.asp'
        ).content,
        'html.parser',
    )
    table = page.find('table', {'id': 'noc'}).find('tbody')
    with open(DATA_FILE, 'w+') as csv:
        for item in table.findAll('tr'):
            tds = item.findAll('td')
            anchor = tds[1].find('a')
            data = jobDetails(tds[0].text)
            logging.info('Detaling %s' % (anchor.text))
            row = "%s,%s,%s,%s,%s\n" % (
                tds[0].text,
                anchor.get('href'),
                anchor.text,
                tds[2].text,
                ','.join(data)
            )
            csv.write(row)

def update_list():
    with open(JOBS_FILE) as f:
        jobs = [l.rstrip('\n') for l in f]
        giantSearch(jobs)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG
    )
    # update_list()
    smartDownload()
