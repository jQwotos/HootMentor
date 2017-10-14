import requests

from bs4 import BeautifulSoup

BASE_URL = 'https://www.google.ca/search'


def _scrape_item(data):
    urlBox = data.find('a')
    if urlBox is not None:
        descBox = data.find({'class': 'st'})
        desc = descBox.text if descBox is not None else None
        urlData = urlBox.get('href')
        url = urlData.replace('/url?q=','') if urlData is not None else None
        return {
            'title': urlBox.text,
            'link': urlBox.get('href'),
            'desc': desc,
        }
    else: return None

def _seperate_list(data):
    results = data.find('ol')
    result = [_scrape_item(x) for x in results]

    return list(filter(None, result))

def search(query):
    data = BeautifulSoup(
        requests.get(
            BASE_URL,
            params={'q': query}
        ).content
    )

    result = _seperate_list(data)

    return result
