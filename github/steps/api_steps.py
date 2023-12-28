import requests
from behave import step


@step('API: send {type} request to {endpoint}')
def send_request_to(context, type, endpoint):
    if endpoint.startswith('/'):
        endpoint = endpoint[1:]

    if type.upper() == 'GET':
        response = requests.get(f"{context.BASE_API}/{endpoint}")

    context.request_url = response.url
    context.response = response


@step('API: verify status code is {code:d}')
def verify_status(context, code):
    context.response_body = context.response.json()
    assert context.response.status_code == code, (f'API response code does not match:'
                                                  f'\nExpected: {code}'
                                                  f'\nActual:\t{context.response.status_code}'
                                                  f'\nURL:\t{context.request_url}')
