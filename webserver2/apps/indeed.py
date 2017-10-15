import requests

from bs4 import BeautifulSoup

BASE_URL = 'https://indeed.com'
SEARCH_URL = '%s/jobs' % (BASE_URL,)

def search(query):
    if type(query) == str:
        data = BeautifulSoup(
            requests.get(
                SEARCH_URL,
                params = {
                    ''
                }
            )
        )
    else:
        data = BeautifulSoup(
            requests.get(
                SEARCH_URL,
                params = query.get('')
            )
        )
