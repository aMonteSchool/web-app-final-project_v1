from behave import register_type

from uhaul.components.order_models.bike_racks_order import BikeRacksOrder
from uhaul.components.order_models.storage_order import StorageOrder
from uhaul.components.order_models.truck_order import TruckOrder
from uhaul.components.trucks.boxes_option import BoxesOption
from uhaul.components.trucks.dollies_option import DolliesOption
from uhaul.components.trucks.moving_option import MovingOption
from uhaul.components.trucks.storage_units import StorageUnitsOption


def select_order_type(order_type: str) -> TruckOrder | StorageOrder | BikeRacksOrder:
    order_map = {
        'truck': TruckOrder,
        'storage': StorageOrder,
        'bike racks': BikeRacksOrder
    }
    try:
        return order_map[order_type.lower()]
    except KeyError:
        raise ValueError("Incorrect order type provided."
                         "\nCorrect types: ['Truck', 'Storage', 'Bike Racks']")


def select_options_page(option_page: str) -> DolliesOption | StorageUnitsOption | BoxesOption | MovingOption:
    page_map = {
        'dollies': DolliesOption,
        'storage units': StorageUnitsOption,
        'boxes & packing': BoxesOption,
        'moving loading': MovingOption,
        'moving unloading': MovingOption
    }
    try:
        return page_map[option_page.lower()]
    except KeyError:
        raise ValueError("Incorrect Option Page provided."
                         "\nCorrect pages: [Dollies, Storage Units, Boxes & Packing, Moving Loading, Moving Unloading]")


def convert_context_var(context, value):
    return getattr(context, value, value)


def get_order(order_type: str) -> TruckOrder | StorageOrder | BikeRacksOrder:
    return select_order_type(order_type)


def get_order_options_page(option_page: str):
    return select_options_page(option_page)


register_type(OrderType=get_order)
register_type(OptionPage=get_order_options_page)
