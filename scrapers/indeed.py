import requests

from bs4 import BeautifulSoup

BASE_URL = 'https://www.indeed.com/jobs'

SEARCH_URL = '%s/jobs' % (BASE_URL,)


def link_combiner(sub):
    return '%s%s' % (BASE_URL, sub,)

def _posting_to_text(data):
    summaryBox = data.find('span', {'id': 'job_summary'})
    return summary.text

def postingToText(link):
    data = BeautifulSoup(
        requests.get(
            link
        )
    )

    return _posting_to_text(data)


def _scrape_item(data):
    urlBox = data.find('a')
    companyBox = data.find('span', {'itemprop': 'name'})
    link = link_combiner(urlBox.get('href'))
    if urlBox is not None:
        return {
            'link': urlBox.get('href'),
            'title': urlBox.text,
            'company': companyBox.text,
            'text': postingToText(link),
        }

def _seperate_list(data):
    results = data.find('td', {'id': 'resultsCol'})
    return [_scrape_item(x) for x in results]

def search(query):
    data = BeautifulSoup(
        requests.get(
            SEARCH_URL,
            params={'q': query}
        ).content,
        'html.parser'
    )
    result = _seperate_list(data)

    
