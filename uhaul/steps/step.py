import logging
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
from uhaul.components.order_models.ubox_order import UboxOrder
from uhaul.components.storage.result_filter import ResultFilter
from uhaul.components.storage.select_storage import Storage
from uhaul.components.trucks.boxes_option import BoxesOption
from uhaul.components.trucks.damage_protection import DamageProtection
from uhaul.components.trucks.dollies_option import DolliesOption
from uhaul.components.trucks.hitches_and_accessories import HitchesAndAccessories
from uhaul.components.trucks.location_select import SelectLocation
from uhaul.components.trucks.main_screen import MainScreen
from uhaul.components.trucks.moving_option import MovingOption
from uhaul.components.trucks.shopping_cart import ShoppingCart
from uhaul.components.trucks.storage_units import StorageUnitsOption
from uhaul.components.trucks.truck_rates import Rates
from uhaul.components.trucks.truck_with_towing import TruckWithTowing
from uhaul.components.ubox.ubox import UBoxOption
from uhaul.components.ubox.ubox_boxes_and_packing import UBoxSuppliers
from uhaul.components.ubox.ubox_loading_help import UBoxLoadingHelp

logger = logging.getLogger('Step Def')



@step('Create a new {order_type:OrderType} order')
def create_new_order(context, order_type: Type[TruckOrder | StorageOrder | BikeRacksOrder | UboxOrder]) -> None:
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


@when("Select the truck with towing")
def step_impl(context: Context):
    context.options = ContextTable(context).to_flat_dict()
    TruckWithTowing(context.browser, context.order).select_truck_with_towing(context.options)


@Step('Select closest truck {feature}')
@step('Select closest truck')
def select_closest_truck(context: Context, feature: str = None) -> None:
    location = SelectLocation(context.browser, context.order)
    location.select_dropdown_option(SelectLabels.PICKUP_TIME)
    location.select_closest_truck()

    if feature != 'with towing':
        HowPickUp(context.browser).select_option(HowPickUpOptions.MOBILE)
    else:
        DamageProtection(context.browser, context.order).collect_trailer_coverage()

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
    ShoppingCart(context.browser, context.order).collect_vehicle_license_recovery()
    ShoppingCart(context.browser, context.order).collect_moving_fee()
    ShoppingCart(context.browser, context.order).verify_price_due_at_pickup()
    # with open("price_validation_screenshot.png", "rb") as file:
    #     png_content = file.read()
    #
    #
    # logger.info("Log message with PNG attachment", {
    #     "name": "screenshot.png",
    #     "data": png_content,
    #     "mime": "image/png",
    # })


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


@when("Select storage")
def select_storage(context):
    Storage(context.browser, context.order).select_storage(ContextTable(context).to_flat_dict())


@step("Select unit")
def select_unit(context):
    Storage(context.browser, context.order).select_storage_unit(ContextTable(context).to_flat_dict())


@step("Select insurance")
def select_insurance(context):
    Storage(context.browser, context.order).select_insurance(ContextTable(context).to_flat_dict())


@then("Verify Shopping Cart Self-Storage Rental")
def verify_card_self_storage(context):
    ShoppingCart(context.browser, context.order).verify_price_self_storage()


@when("I open Hitches & Accessories")
def step_impl(context):
    MainScreen(context.browser, context.order).open_hitches_and_accessories()


@step("I open Shop Bike Racks")
def step_impl(context):
    HitchesAndAccessories(context.browser, context.order).select_bike_rack()


@when("I select Bike Rack")
def step_impl(context):
    context.options = ContextTable(context).to_flat_dict()
    BikeRacks(context.browser, context.order).select_bike_rack(context.options)


@step("I click Add to Cart")
def step_impl(context):
    BikeRacks(context.browser, context.order).click_add_to_card()


@step("I click View Cart")
def step_impl(context):
    BikeRacks(context.browser, context.order).click_vew_cart()


@then("Verify Shopping Cart for Bike Rack")
def step_impl(context):
    ShoppingCart(context.browser, context.order).verify_price_bike_rack()


@step("I select Ship to me delivery")
def step_impl(context):
    BikeRacks(context.browser, context.order).select_ship_to_me_option()


@step("Open UBox")
def step_impl(context):
    MainScreen(context.browser, context.order).open_ubox();


@step("Get rates for Ranked Moving Container")
def step_impl(context):
    context.options = ContextTable(context).to_flat_dict()
    UBoxOption(context.browser, context.order).get_ranked_container_rates(context.options)


@step("Select {container_count} containers and collect prices")
def step_impl(context, container_count):
    UBoxOption(context.browser, context.order).select_containers_count(container_count)


@step("Plan Ubox move")
def step_impl(context):
    context.options = ContextTable(context).to_flat_dict()
    UBoxOption(context.browser, context.order).plan_ubox_move(context.options)


@step("Select delivery option")
def step_impl(context):
    context.options = ContextTable(context).to_flat_dict()
    UBoxOption(context.browser, context.order).select_delivery_option(context.options)


@step("I {action} Need Help Loading Your Items")
def step_impl(context, action):
    match action.lower():
        # case 'add':
            # todo implement
        case 'skip':
            UBoxLoadingHelp(context.browser, context.order).skip_page()


@step("I {action} Boxes & Packing Supplies")
def step_impl(context, action):
    match action.lower():
        # case 'add':
        # todo implement
        case 'skip':
            UBoxSuppliers(context.browser, context.order).skip_page()


@step("I Select Ubox Coverage")
def step_impl(context):
    context.options = ContextTable(context).to_flat_dict()
    UBoxOption(context.browser, context.order).select_coverage(context.options)


@then("Verify Shopping Cart for UBox order")
def step_impl(context):
    ShoppingCart(context.browser, context.order).verify_ubox_order_price()
