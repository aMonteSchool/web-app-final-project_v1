import time

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.select import Select

from fractions import Fraction

from uhaul.components.trucks.order_option import OrderOption
from uhaul.components.order_models.truck_order import TruckOrder
from uhaul.components.order_models.storage_order import StorageOrder
from typing import Type


class DolliesOption(OrderOption):
    BUTTON_ADD = '//button[@id="btnAddUpdateSRI"]'
    ITEMS = '//li[@class="cell text-center"]'
    ITEM = ITEMS + '//h4[contains(text(),"{option}")]'
    PRICE = ITEM + '//following-sibling::p'
    AMOUNT_OPTION = ITEM + '/ancestor::li//select'

    def __init__(self, driver: WebDriver, order: Type[TruckOrder | StorageOrder] = None):
        super().__init__(driver)
        self.order = order
        self.selectors = ['Utility Dolly', 'Appliance Dolly', 'Furniture Dolly', 'Furniture Pads']

    def add_option(self, options):
        # Set amount of all options on the page to '0'
        for selection in self.selectors:
            select = Select(self.find_element(self.AMOUNT_OPTION.format(option=selection)))
            select.select_by_visible_text('0')

        # Select option and set its amount from test data, collect price
        for key, value in options.items():
            select = Select(self.find_element(self.AMOUNT_OPTION.format(option=key)))
            select.select_by_visible_text([option.text for option in select.options if value in option.text][0])

            price_str = (self.find_element(self.PRICE.format(option=key)).text.replace('$', '')).split(
                ' ')[0]
            amount = Fraction(eval(value.split(' ')[0]))
            price = float(price_str) * float(amount)

            self.order.truck_price_records |= {key: price}

        self.click(self.BUTTON_ADD)
