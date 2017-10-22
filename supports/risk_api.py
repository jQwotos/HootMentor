import re
import logging

import requests
from bs4 import BeautifulSoup as bs

import requests_toolbelt.adapters.appengine

from database import JobRisk


def _nocRiskDB(noc_code):
    dbEntry = JobRisk.query(
        JobRisk.noc_code == noc_code
    ).fetch(1)

    if len(dbEntry) > 0:
        return dbEntry[0].automation_risk

    return None


def nocRisk(noc_code):
    dbRisk = _nocRiskDB(noc_code)
    if dbEntry is not None:
        return dbEntry
    else:
        return '0'
