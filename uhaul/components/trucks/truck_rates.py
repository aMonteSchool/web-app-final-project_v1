from datetime import datetime

from selenium.common import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver

from base.components.base import Base
from uhaul.components.order_models.truck_order import TruckOrder


class Rates(Base):
    TRUCKS = '//ul[@id="equipmentList"]/li'
    A_TRUCK = TRUCKS + '[.//h3[starts-with(normalize-space(.), "{size}")]]'
    SELECT_BUTTON = A_TRUCK + '//button'
    TRUCK_PRICE = A_TRUCK + '//b'

    def __init__(self, driver: WebDriver, order: TruckOrder):
        super().__init__(driver)
        self.order = order
        self.sizes = ['Small', '8', '9', '10', '15', '17', '20', '26']

    def select_truck(self):
        self.collect_price()
        self.find_element(self.SELECT_BUTTON.format(size=self.order.truck_size)).click()

    def collect_price(self):
        price = float(self.find_element(self.TRUCK_PRICE.format(size=self.order.truck_size)).text.replace('$', ''))

        self.order.truck_price_records |= {"rate": price}

    def verify_all_size_rates_present(self):
        present_trucks = []
        for size in self.sizes:
            try:
                present = bool(self.find_element(self.TRUCKS.format(size=size)))
            except TimeoutException:
                present = False
            present_trucks.append(present)

    def verify_header(self):
        header = self.find_element('//h1')
        date = datetime.strptime(self.order.pick_up_date, "%m.%d.%Y").strftime("%m/%d/%Y").lstrip('0')
        assert header.text.lower() == (f"Rates for {self.order.pick_up_city} on {date}".lower())
