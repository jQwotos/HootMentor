import re
import logging

import requests
from bs4 import BeautifulSoup as bs

import requests_toolbelt.adapters.appengine

from database import JobRisk

from google.appengine.ext import ndb


def _noc_risk_db(noc_code):
    dbEntry = JobRisk.query(
        JobRisk.noc_code == noc_code
    ).fetch(1)

    if len(dbEntry) > 0:
        return dbEntry[0].automation_risk

    return None


def noc_risk(noc_code):
    dbRisk = _nocRiskDB(noc_code)
    if dbEntry is not None:
        return dbEntry
    else:
        return '0'


def add_multi_db(items):
    # Adds many risk to db
    current = [
    str(x.noc_code)
    for x in JobRisk.query().fetch()
    ]
    itemObjs = []
    for item in items:
        if item is not on current:
            itemObjs.append(
                JobRisk(
                    noc_code = item.get('noc'),
                    automation_risk = float(item.get('automation_risk'))
                ))
    ndb.put_multi(itemObjs)
