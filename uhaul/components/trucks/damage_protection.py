from typing import Type

from selenium.webdriver.chrome.webdriver import WebDriver

from base.components.base import Base
from uhaul.components.order_models.storage_order import StorageOrder
from uhaul.components.order_models.truck_order import TruckOrder


class DamageProtection(Base):
    BUTTON_CONTINUE = '//button[@id="btnContinueSafeTrip"]'
    BUTTON_CLOSE = ''
    COVERAGE = '//ul[@id="coverageList_Truck"]/li'
    COVERAGE_PRICE = COVERAGE + '//dd//strong'
    TRAILER_RENTAL_COVERAGE_PRICE = '//ul[@id = "coverageList_Trailer"]//strong[@class ="text-xl text-callout medium-text-base"]'

    def __init__(self, driver: WebDriver, order: Type[TruckOrder | StorageOrder] = None):
        super().__init__(driver)
        self.order = order

    def press_continue(self):
        self.find_element(self.BUTTON_CONTINUE).click()

    def collect_price(self):
        price = float(self.find_element(self.COVERAGE_PRICE.format(size=self.order.truck_size)).text.replace('$', ''))

        self.order.truck_price_records |= {"coverage": price}

    def collect_trailer_coverage(self):
        price = float(self.find_element(self.TRAILER_RENTAL_COVERAGE_PRICE.format(size=self.order.truck_size)).text.replace('$', ''))

        self.order.truck_price_records |= {"trailer_coverage": price}

