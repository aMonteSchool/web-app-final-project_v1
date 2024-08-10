from behave.runner import Context

from base.environment import hooks
from uhaul.components.constant import URL
from uhaul.helpers.register_types import register_type
from base.steps import browser_steps


def before_feature(context, feature):
    context.u_haul = URL.U_HAUL


def before_scenario(context, scenario):
    hooks.before_scenario(context, scenario)
