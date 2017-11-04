import re
import logging

import requests
from bs4 import BeautifulSoup as bs

from google.appengine.api import urlfetch
import requests_toolbelt.adapters.appengine

from database import JobPosting

BASE_URL = 'https://www.jobbank.gc.ca/'
SEARCH_URL = '%sjobsearch/feed/jobSearchRSSfeed' % (BASE_URL,)
POSTING_URL = '%sjobposting' % (BASE_URL,)

NOC_NO_PAT = r'<span class="noc-no">NOC ([0-9]+)</span>'
JOB_NO_PAT = r'([0-9]+)$'

REPORT_URL = '%sreport-eng.do' % (BASE_URL,)

report_params = {
    'area': '25565',
    'lang': 'eng',
    'ln': 'n',
    'action': 'final',
}

requests_toolbelt.adapters.appengine.monkeypatch()


def _job_number_to_noc_code(job_number):
    # Scrapes the noc code using a job number
    # by scraping the job posting.
    data = requests.get(
        '%s/%s' % (POSTING_URL, job_number)
    ).content
    '''
    data = urlfetch.fetch(
        '%s/%s' % (POSTING_URL, job_number)
    )
    '''
    noc_code = re.search(NOC_NO_PAT, data)
    logging.debug("Scraped job #%s."%(job_number,))
    if noc_code is not None:
        return re.findall(NOC_NO_PAT, noc_code.group())[0]
    return None


def _extract_job_number_from_url(url):
    # Extracts the job number from a jobbank url
    # using regex pattern
    job_number = re.search(JOB_NO_PAT, url)
    return job_number.group() if job_number is not None else None


def search(query_string, **properties):
    # Searches jobbank using title of job and properties

    # Params are the params in the get request
    params = {
        'searchstring': query_string,
        'sort': 'M',
        'lang': 'en',
        # 'action': 's1',
        # 'fss': properties.get('education_level'),
        # 'fcat': properties.get('job_category'),
    }
    request = requests.get(SEARCH_URL, params = params)
    # request = urlfetch.fetch(SEARCH_URL, params)
    # if request.status_code == requests.codes.ok:
    if request.status_code == 200:
        # Data is the BeautifulSoup parsed version
        # of the results
        data = bs(request.content, "lxml")
        return data
    return None

def noc_to_title(query_string):
    pat = r'<\!\[CDATA\[(.*)]]>'
    data = search(query_string)
    all_postings = data.findAll('entry')
    if len(all_postings) > 0:
        leading_entry = all_postings[0]
        title = leading_entry.find('title').text
        return re.findall(pat, title)[0]


def _cached_job_number_to_noc(job_number):
    # Uses the stored database to find
    # noc code from job number,
    # will also add into database if not exists,
    # and still return job number
    posting = JobPosting.query(
        JobPosting.job_code == job_number
    ).fetch(1)
    if len(posting) == 0:
        # If the job number does not exists in database
        # Scrape for it's noc number
        noc_code = _job_number_to_noc_code(job_number)
        if noc_code is not None:
            # Add to database if exists
            jobPosting = JobPosting(
                noc_code = noc_code,
                job_code = job_number)
            # Commits the addin to the database
            jobPosting.put()
            # Return noc_code
            return noc_code
    else:
        # If the job number does exists in database,
        # return noc code
        return posting[0].noc_code
    return None

'''
def noc_to_job_title(noc_code):
    databaseJobs = NocJob.query(
        NocJob.noc_code == noc_code
    ).fetch(1)

    if len(databaseJobs) == 0:
        # If the job does not exists in the database
        # scrape and add it

    else:
        return databaseJobs[0].title
    return None
'''

def _url_to_noc(link):
    # Takes in a jobbank link and returns noc code
    return _cached_job_number_to_noc(
                _extract_job_number_from_url(
                    link
                )
            )


def find_similar(query_string):
    # Finds similar jobs based on name of a job
    search_result = search(query_string)
    if search_result is not None:
        all_postings = search_result.findAll('entry')
        if len(all_postings) > 0:
            leading_entry = {'entry_object': all_postings[0]}
            leading_entry['job_number'] = _extract_job_number_from_url(
                leading_entry['entry_object'].find('link').get('href'))
            leading_entry['noc_code'] = _job_number_to_noc_code(
                leading_entry['job_number'])

            return [x for x in (
                        _url_to_noc(y.find('link').get('href'))
                        for y in all_postings
                        )
                    if x != leading_entry.get('noc_code')
            ]

    return None

def clean_text(text):
    return str(re.sub('\s\s+', '', text))

def _parse_wage_row(row):
    wages = row.findAll('td', {'headers': 'header2_wages_nat'})
    result = {
        'area': clean_text(row.find('td', {'class': 'area'}).text)
    }
    for w in wages:
        result[w.get('class')[0]] = clean_text(str(w.text))
    return result

def _parse_wage_table(table):
    rows = table.findAll('tr', {'class': 'province'})
    rows.append(table.find('tr', {'class': 'national'}))
    return [_parse_wage_row(x) for x in rows]


def scrape_report_wages(*noc_code):
    report_params['s'] = '1'
    if len(noc_code) > 0:
        report_params['noc'] = noc_code[0]
    print('Sending request for report wages for %s' % (report_params['noc'],))
    print(REPORT_URL)
    print(report_params)
    data = bs(requests.get(
        REPORT_URL,
        params=report_params
    ).content)
    print('Finished request for report wages for %s' % (report_params['noc'],))
    table = data.find('table', {'id': 'natwagetable'})
    if table is not None:
        return _parse_wage_table(table)

    return None

def _parse_education_row(row):
    anchor = row.find('a')
    return {
        'link': str(anchor.get('href')),
        'title': str(anchor.text)
    }

def _parse_education_table(table):
    rows = table.findAll('li')
    return [
            _parse_education_row(x) for x in rows
    ]

def scrape_report_education(*noc_code):
    report_params['s'] = '3'
    if len(noc_code) > 0:
        report_params['noc'] = noc_code[0]
    data = bs(requests.get(
        REPORT_URL,
        params=report_params
    ).content,'html.parser')
    if data is not None:
        table = data.findAll('div', {'class': 'ReportArticle'})
        if len(table) >= 3:
            return _parse_education_table(table[2])


def scrape_report_details(noc_code):
    report_params['noc'] = noc_code
    return {
        'wages': scrape_report_wages(),
        'education_programs': scrape_report_education(),
    }
