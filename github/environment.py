import chrome


def before_feature(context, feature):
    context.BASE_URL = f'https://gh-users-search.netlify.app'
    context.BASE_API = f'https://api.github.com'


def before_scenario(context, scenario):
    if chrome.is_alive(context):
        chrome.close(context)
    chrome.init(context)
    chrome.info(context)


def after_step(context, step):
    print('STEP\t\t', step.name, '\t', step.status)
    if step.status == 'failed':
        chrome.take_screenshot(context)


def after_scenario(context, scenario):
    print('SCENARIO\t', scenario.name, '\t', scenario.status)
    chrome.close(context)
