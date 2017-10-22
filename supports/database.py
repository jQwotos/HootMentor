import logging

from google.appengine.ext import ndb
from uuid import uuid4

class JobPosting(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add = True)
    noc_code = ndb.StringProperty(required = True)
    job_code = ndb.StringProperty(required = True)

class NocJob(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add = True)
    noc_code = ndb.StringProperty(required = True)
    title = ndb.StringProperty(required = True)

class JobRisk(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add = True)
    noc_code = ndb.StringProperty(required = True)
    automation_risk = ndb.FloatProperty(required = True)
