import requests

from bs4 import BeautifulSoup

def getNParse(link, *params):
    return BeautifulSoup(
        requests.get(
            link,
            params = params if params else None
        ).content,
        'html.parser'
    )
