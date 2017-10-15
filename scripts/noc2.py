import re
import logging

import requests
from bs4 import BeautifulSoup

URL = 'http://www.cic.gc.ca/english/immigrate/skilled/noc.asp'

def _parse_single(data):
    tds = data.findAll('td')
    return {
        'noc_code': tds[0],
        'level': tds[2].text,
    }

def _seperate(data):
    items = data.findAll('tr')[1:]
    return [_parse_single(x) for x in items]

def scrape():
    page = BeautifulSoup(
        requests.get(URL).content,
        'html.parser',
    )
    return _seperate(page)
