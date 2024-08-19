from behave import step


@step('Browser: navigate to Github')
def navigate_to_url(context):
    """
    Navigate to url
    """
    context.browser.get('/'.join([path.strip('/') for path in context.BASE_URL.split('/')]))
