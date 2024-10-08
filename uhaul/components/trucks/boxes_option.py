from typing import Optional, Dict

from selenium.webdriver.chrome.webdriver import WebDriver

from uhaul.components.order_models.truck_order import TruckOrder
from uhaul.components.trucks.order_option import OrderOption


class BoxesOption(OrderOption):

    def __init__(self, driver: WebDriver, order: TruckOrder = None):
        super().__init__(driver)

    def add_option(self, options: Optional[Dict[str, str]] = None):
        pass
