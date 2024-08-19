import requests
from behave import step

from base.helpers.helper import map_url


@step('API: send {type} request to {endpoint}')
def send_request_to(context, type, endpoint):
    url_, part_url = endpoint.split('/', 1)
    base_url = map_url(url_)
    url = base_url + part_url

    response = None
    if type.upper() == 'GET':
        response = requests.get(url)

    context.request_url = response.url
    context.response = response


@step('API: verify status code is {code:d}')
def verify_status(context, code):
    context.response_body = context.response.json()
    assert context.response.status_code == code, (f'API response code does not match:'
                                                  f'\nExpected: {code}'
                                                  f'\nActual:\t{context.response.status_code}'
                                                  f'\nURL:\t{context.request_url}')
