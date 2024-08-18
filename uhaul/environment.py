from behave.runner import Context
from base.environment import hooks
from uhaul.components.constant import URL
from uhaul.helpers.register_types import register_type
from base.steps import browser_steps


def before_all(context):
    hooks.before_all(context)


def before_feature(context, feature):
    hooks.before_feature(context, feature)
    context.u_haul = URL.U_HAUL


def before_scenario(context, scenario):
    hooks.before_scenario(context, scenario)


def before_step(context, step):
    hooks.before_step(context, step)


def after_step(context, step):
    hooks.after_step(context, step)


def after_scenario(context, scenario):
    hooks.after_scenario(context, scenario)


def after_feature(context, feature):
    hooks.after_feature(context, feature)
    context.u_haul = URL.U_HAUL


def after_all(context):
    hooks.after_all(context)
