import logging
import json

import endpoints

from protorpc import message_types
from protorpc import messages
from protorpc import remote

import supports.jobbank_api as jbapi
import supports.risk_api as rkapi
import supports.crypto_verify as crypto


class JobSearchRequest(messages.Message):
    content = messages.StringField(1)

class JobSearchResponse(messages.Message):
    content = messages.StringField(1)


JOB_RESOURCE = endpoints.ResourceContainer(
    JobSearchRequest,
    n=messages.IntegerField(2, default=1)
)


# Endpoint API class for /_ah/api/jobSearch/v1
@endpoints.api(name='jobSearch', version='v1')
class JobSearchApi(remote.Service):

    # /_ah/api/jobSearch/v1/jobSearch/echo
    # Requires {'content': 'anything'}; returns {'content': 'anything'}
    @endpoints.method(
        JOB_RESOURCE,
        JobSearchResponse,
        path='jobSearch/echo',
        http_method='POST',
        name='echo')
    def echo(self, request):
        output_content = ' '.join([request.content] * request.n)
        return JobSearchResponse(content=output_content)

    # /_ah/api/jobSearch/v1/jobSearch/findSimilar
    # Requires {'content': 'job title'}; returns {'content': "['list', 'jobs']"}
    @endpoints.method(
        JOB_RESOURCE,
        JobSearchResponse,
        path='jobSearch/findSimilar',
        http_method='POST',
        name='find_similar')
    def find_similar(self, request):
        result = jbapi.find_similar(str(request.content))
        output_content = ' '.join([str(result)] * request.n)
        return JobSearchResponse(content=output_content)

    # /_ah/api/jobSearch/v1/jobSearch/marketReportDetails
    # Refer to README.md for usage
    @endpoints.method(
        JOB_RESOURCE,
        JobSearchResponse,
        path='jobSearch/marketReportDetails',
        http_method='POST',
        name='market_report_details')
    def market_report_details(self, request):
        received = str(request.content)
        result = jbapi.scrape_report_details(received)
        output_content = ' '.join([str(result)] * request.n)
        return JobSearchResponse(content=output_content)

    # /_ah/api/jobSearch/v1/jobSearch/nocRisk
    # Requires {'content': 'noc_code'}; returns {'content': 'job risk'}
    @endpoints.method(
        JOB_RESOURCE,
        JobSearchResponse,
        path='jobSearch/nocRisk',
        http_method='POST',
        name='noc_risk')
    def noc_risk(self, request):
        recieved = str(request.content)
        result = rkapi.noc_risk(recieved)
        output_content = ' '.join([str(result)] * request.n)
        return JobSearchResponse(content=output_content)

    @endpoints.method(
        JOB_RESOURCE,
        JobSearchResponse,
        path='jobSearch/dbAdd',
        http_method='POST',
        name='db_add')
    def db_add(self, request):
        recieved = json.loads(request.content)
        if crypto.verify(recieved.get('password')):
            rkapi.add_multi_db(recieved.get('data'))
            result = 'Successfully added data points!'
        else:
            result = 'Falsed to verify key.'
        output_content = ' '.join([result] * request.n)
        return JobSearchResponse(content=output_content)

api = endpoints.api_server([JobSearchApi])
