from github.context_table import to_list_of_dicts
from behave import step
from github.helpers import message

from github.components.summary import Summary
from github.components.user import User
from github.components.followers import Followers


@step('GitHub Integration API: {component}: verify param values')
def integration_verify_ui_vs_api(context, component):
    params = to_list_of_dicts(context)
    component = component.lower()

    if component == 'followers':
        instance = Followers(context.driver)
    elif component == 'user':
        instance = User(context.driver)
    elif component == 'summary':
        instance = Summary(context.driver)

    for param in params:
        label = param.get('label').lower()

        ui_value = instance.get_elements_text_by_label(label)
        api_value = instance.eval_json_path_by_label(context.response_body, label)

        if api_value and label == 'twitter':
            api_value = instance.compute_twitter(api_value)

        assert api_value == ui_value, message(label, api_value, ui_value)


@step('GitHub Integration API: verify navigation link for {what}')
def integration_verify_ui_vs_api(context, what):
    what = what.lower()
    what_list = ["follow", "blog", "followers"]
    assert what in what_list, f'Script: {what} should be in {what_list}'

    if what == 'follow':
        instance = User(context.driver)
        api_urls = instance.eval_json_path_by_label(context.response_body, what)
    elif what == 'blog':
        instance = User(context.driver)
        values = instance.eval_json_path_by_label(context.response_body, what)
        api_urls = instance.compute_blog(values)
    elif what == 'followers':
        what = 'links'
        instance = Followers(context.driver)
        api_urls = instance.eval_json_path_by_label(context.response_body, what)

    ui_urls = instance.get_elements_href_by_label(what)

    assert ui_urls == api_urls, message(what, api_urls, ui_urls)


@step('GitHub Integration API: Followers: verify total amount')
def integration_verify_ui_vs_api(context):
    instance = Followers(context.driver)

    api_amount = len(context.response_body)

    ui_values = instance.get_followers_elements()
    if not ui_values:
        ui_amount = 0
    else:
        ui_amount = len(ui_values)

    assert api_amount == ui_amount, message('Followers total amount', api_amount, ui_amount)
