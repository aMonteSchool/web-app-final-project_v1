from typing import Dict

from selenium.webdriver.chrome.webdriver import WebDriver

from base.components.base import Base


class Trucks(Base):
    """Truck selection page"""

    TRUCK_ITEM = '//div[@class="grid-x grid-padding-x"][.//button][contains(., "{size}")]'

    def __init__(self, driver: WebDriver, size: str):
        """
        :param WebDriver driver: Selenium Web Driver object
        :param str size: Size of a Truck to select
        """
        super().__init__(driver)
        self.size = size
        self.order: Dict = {}

    def add_price(self):
        """Collect price for further calculation"""

        price = self.find_element(f"{self.TRUCK_ITEM.format(size=self.size)}//b")
        price = float(price.text.replace('$', ''))
        self.order |= {self.size: price}

    def select_truck(self):
        """Selects the desired Truck"""

        self.add_price()
        self.find_element(f'{self.TRUCK_ITEM.format(self.size)}//button').click()
