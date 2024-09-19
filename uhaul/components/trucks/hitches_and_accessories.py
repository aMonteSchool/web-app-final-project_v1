from base.components.base import Base
from selenium.webdriver.chrome.webdriver import WebDriver
from uhaul.components.order_models.bike_racks_order import BikeRacksOrder


class HitchesAndAccessories(Base):

    BIKE_RACK = '//a[contains(@href, "Bike-Rack") and contains(@class, "button")]'

    def __init__(self, driver: WebDriver, order: BikeRacksOrder = None):
        super().__init__(driver)
        self.order = order

    def select_bike_rack(self):
        self.find_element(self.BIKE_RACK).click()

