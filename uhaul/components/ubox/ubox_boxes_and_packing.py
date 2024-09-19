from selenium.webdriver.chrome.webdriver import WebDriver
from uhaul.components.order_models.ubox_order import UboxOrder
from uhaul.components.trucks.order_option import OrderOption

class UBoxSuppliers(OrderOption):

    def __init__(self, driver: WebDriver, order: UboxOrder = None):
        super().__init__(driver)
        self.order = order


