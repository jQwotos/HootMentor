import requests
import re

from bs4 import BeautifulSoup

BASE_URL = 'https://www.jobbank.gc.ca'

SEARCH_URL = '%s/jobsearch/jobsearch' % BASE_URL


def _clean_text(text):
    sub1 = re.sub('[\n\t]', '', text)
    return re.sub('[ ]{2,}', '', sub1)

def _scrape_item(data):
    urlBox = data.find('a')
    if urlBox is not None:
        print(urlBox)
        detailList = urlBox.find('ul', {'class': 'list-unstyled'})
        details = [
            {
                'type': x.find('span', {'class': 'wb-inv'}).text,
                'value': _clean_text(x.text),
            } for x in detailList.findAll('li')
        ]
        return {
            'title': _clean_text(urlBox.find('h3', {'class': 'title'}).text),
            'link': "%s%s" % (BASE_URL, urlBox.get('href'),),
            'details': details,
        }


def _seperate_list(data):
    results = data.findAll('div', {'class': 'results-jobs'})
    return [_scrape_item(x) for x in results]

def search(query):
    data = BeautifulSoup(
        requests.get(
            SEARCH_URL,
            params = {'fn': query} if len(query) == 4 else {'searchstring': query}
        ).content,
        'html.parser'
    )

    return _seperate_list(data)
