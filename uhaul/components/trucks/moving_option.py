from selenium.webdriver.chrome.webdriver import WebDriver

from uhaul.components.order_models.truck_order import TruckOrder
from uhaul.components.trucks.order_option import OrderOption


class MovingOption(OrderOption):

    def __init__(self, driver: WebDriver, order: TruckOrder = None):
        super().__init__(driver)

    def add_option(self):
        pass
