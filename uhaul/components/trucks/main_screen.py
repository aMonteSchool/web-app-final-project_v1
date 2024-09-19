from base.components.base import Base
from selenium.webdriver.chrome.webdriver import WebDriver
from uhaul.components.order_models.bike_racks_order import BikeRacksOrder


class MainScreen(Base):

    HITCHES_AND_ACCESSORIES = '//a[contains(text(), "Hitches & Accessories") and contains(@class, "show")]'
    UBOX = '//a[contains(@href, "UBox") and contains(@class, "show")]'


    def __init__(self, driver: WebDriver, order: BikeRacksOrder = None):
        super().__init__(driver)
        self.order = order

    def open_hitches_and_accessories(self):
        self.find_element(self.HITCHES_AND_ACCESSORIES).click()


    def open_ubox(self):
        self.find_element(self.UBOX).click()


