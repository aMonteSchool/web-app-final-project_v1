from typing import Type, Optional

from behave import *
from behave.runner import Context

from base.components.behave_support import BehaveSupport as BS
from base.components.context_table import ContextTable
from uhaul.components.bike_racks.bike_racks import BikeRacks
from uhaul.components.constant import SelectLabels, HowPickUpOptions
from uhaul.components.hero_form import HeroForm
from uhaul.components.how_pickup import HowPickUp
from uhaul.components.modal import Modal
from uhaul.components.order_models.bike_racks_order import BikeRacksOrder
from uhaul.components.order_models.storage_order import StorageOrder
from uhaul.components.order_models.truck_order import TruckOrder
from uhaul.components.storage.result_filter import ResultFilter
from uhaul.components.trucks.boxes_option import BoxesOption
from uhaul.components.trucks.damage_protection import DamageProtection
from uhaul.components.trucks.dollies_option import DolliesOption
from uhaul.components.trucks.location_select import SelectLocation
from uhaul.components.trucks.moving_option import MovingOption
from uhaul.components.trucks.shopping_cart import ShoppingCart
from uhaul.components.trucks.storage_units import StorageUnitsOption
from uhaul.components.trucks.truck_rates import Rates


@step('Create a new {order_type:OrderType} order')
def create_new_order(context, order_type: Type[TruckOrder | StorageOrder | BikeRacksOrder]) -> None:
    BS(context).set_context_var('order', order_type())
    context.order.set_data(ContextTable(context).to_flat_dict())


@step('Fill Out Hero form {tab}')
def fill_out_hero_form(context, tab: str) -> None:
    HeroForm(context.browser, tab).fill_form(context.order)


@step('Validate {_} checked boxes')
def validate_filter_selected(context, _) -> None:
    ResultFilter(context.browser).verify_checked_options(**ContextTable(context).to_flat_dict())


@step('Verify {data} on {page} page')
def validate_filter_selected(context, data: str, page: str) -> None:
    SelectLocation(context.browser, context.order).verify_data(data)


@step('Verify header on the page {page}')
def verify_header(context: Context, page: str) -> None:
    match page.lower():
        case 'rates':
            Rates(context.browser, context.order).verify_header()
        case 'bike racks':
            BikeRacks(context.browser, context.order).verify_header()


@step('Select the truck rate')
@step('Select the truck rate {size}')
def select_truck_rate(context: Context, size: Optional[str] = None) -> None:
    if size:
        context.order.truck_size = size
    Rates(context.browser, context.order).select_truck()


@step('Select closest truck')
def select_closest_truck(context: Context) -> None:
    location = SelectLocation(context.browser, context.order)
    location.select_dropdown_option(SelectLabels.PICKUP_TIME)
    location.select_closest_truck()

    HowPickUp(context.browser).select_option(HowPickUpOptions.MOBILE)
    DamageProtection(context.browser, context.order).collect_price()
    DamageProtection(context.browser, context.order).press_continue()
    Modal(context.browser).close_modal()


@step('{action} options on page {page:OptionPage}')
def add_order_options(context: Context, action: str,
                      page: Type[DolliesOption | StorageUnitsOption | BoxesOption | MovingOption]) -> None:
    assert action.lower() in {'add', 'skip'}
    page(context.browser).find_element(page.NO_THANKS)
    # sleep(3)  # TODO: Convert into a proper wait for the page to load
    match action.lower():
        case 'add':
            context.options = ContextTable(context).to_flat_dict()
            page(context.browser, context.order).add_option(context.options)
        case 'skip':
            page(context.browser).skip_page()


@step('Verify Shopping Cart Due at Pick Up price')
def verify_cart(context: Context) -> None:
    ShoppingCart(context.browser, context.order).collect_environmental_fee()
    ShoppingCart(context.browser, context.order).verify_price_due_at_pickup()
    with open("price_validation_screenshot.png", "rb") as file:
        png_content = file.read()

    context.log.info("Log message with PNG attachment", attachment={
        "name": "screenshot.png",
        "data": png_content,
        "mime": "image/png",
    })


@when("Set filter on page Bike Racks")
def set_filter(context: Context):
    context.options = ContextTable(context).to_flat_dict()
    BikeRacks(context.browser).set_rack_filter(context.options)


@when("Select from {menu} menu {option} option")
def select_menu_option(context: Context, menu, option):
    BikeRacks(context.browser).select_menu(menu, option)


@step("Verify Results number")
def verify_results_number(context):
    BikeRacks(context.browser).verify_number()
