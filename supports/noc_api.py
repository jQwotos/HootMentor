import re
import logging

import requests
from bs4 import BeautifulSoup as bs

import requests_toolbelt.adapters.appengine

requests_toolbelt.appengine.monkeypatch()

BASE_URL = 'http://noc.esdc.gc.ca/English/noc/'
POSTING_URL = '%sProfileQuickSearch.aspx' % (BASE_URL,)


def noc_code_to_title(noc_code):
    request = requests.get()
    
