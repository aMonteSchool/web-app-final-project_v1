import logging

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


logger = logging.getLogger('driver')


def init(context):
    logger.warning('Initializing Browser\n')

    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    service = Service(ChromeDriverManager(driver_version="117.0.5938.92").install())
    context.browser = webdriver.Chrome(service=service, options=options)


def close(context):
    try:
        context.browser.close()
        context.browser.quit()
    except Exception as e:
        logger.exception(f'Failed to close Chrome browser:\n\t{e.__repr__()}')


def is_alive(context):
    try:
        _ = context.browser.current_url
        return True
    except:
        return False


def take_screenshot(context):
    try:
        return context.browser.get_screenshot_as_png()
    except Exception as e:
        logger.debug(f"Failed to take Chrome screenshot:\n\t{e.__repr__}")


def info(context):
    capabilities = context.browser.capabilities
    logger.debug(f"Browser Info:\n"
                 f"{capabilities['browserName']} "
                 f"{capabilities['browserVersion']}\n"
                 f"driver "
                 f"{capabilities['chrome']['chromedriverVersion'].split(' ')[0]}\n")
