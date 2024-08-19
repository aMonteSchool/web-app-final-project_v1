from time import sleep
from behave import step
from selenium.webdriver import Keys, ActionChains

from github.components.element_base import ElementBase
from github.components.followers import Followers
from github.components.search import Search
from github.components.summary import Summary
from github.components.user import User


@step('UI: search for {username}')
def search_for(context, username):
    if '*space*' in username:
        username = username.replace('*space*', ' ')

    field = Search(context.browser).get_search_field()

    if not field:
        raise ValueError('No Search field found')

    field.send_keys(username)
    field.send_keys(Keys.ENTER)
    sleep(1)


@step('UI: type {username} into Search field')
def type_into_search_field(context, username):
    if '*space*' in username:
        username = username.replace('*space*', '')

    field = Search(context.browser).get_search_field()
    field.send_keys(username)


@step('UI: press {key}')
def press_key(context, key):
    if key.upper() == 'ENTER':
        keys = Keys.ENTER

    ActionChains(context.browser).key_down(keys).perform()


@step('UI: page {condition} empty')
def page_is_empty(context, condition):
    conditions = ['is', 'is not']
    assert condition in conditions, f'Script: {condition} should be in {conditions}'

    is_result = Search(context.browser).is_search_result()

    assert (
            is_result and condition == 'is not' or not is_result and condition == 'is'), f'Expected: {condition}, but is not'


@step('UI: "{action}" {label}')
@step('UI: {component} "{action}" {label}')
def component_click(context, action, label, component=None):
    label = label.lower()
    if component:
        component = component.lower()

        if component == 'followers':
            instance = Followers(context.browser)
        elif component == 'user':
            instance = User(context.browser)
        elif component == 'summary':
            instance = Summary(context.browser)

        element = instance.get_elements_by_label(label)
    else:
        element = ElementBase(context.browser).get_button(label)

    if action == 'click':
        element.click()
    elif action == 'hover':
        ActionChains(context.browser).move_to_element(element).perform()
