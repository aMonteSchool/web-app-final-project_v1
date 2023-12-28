from time import sleep

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.select import Select

from base.components.base import Base

from uhaul.components.order_models.truck_order import TruckOrder


class SelectLocation(Base):
    """Works with Trucks - Select Location page"""
    LOCATION = '//ul[@id="entityList"]/li[contains(normalize-space(.), "{}")]'
    LIST_ITEMS = '//li[contains(@role, "listitem")][not(contains(.//h3, "Alternate"))]'
    ADDRESS = '//address'
    RATING = '//p[@class="rating"]'
    HOURS = '//div[@class="show-for-medium"]//dl'
    TRUCK_SIZE = LIST_ITEMS + '//div[contains(@class, "small-reset-callout")]//dt'
    TRUCK_PRICE = TRUCK_SIZE + '/following-sibling::dd[last() - 1]'
    PICK_UP_DATE = '//label[@class="datepicker"]/input'
    PICK_UP_TIME = '//select[starts-with(@id, "SelectedSchedule")]'
    CONTINUE = LOCATION + '//button[normalize-space(.) = "Continue"]'
    SELECT_HOURS = LOCATION + '//select[starts-with(@id, "HoursNeeded")]'
    SELECT_PICKUP_TIME = LOCATION + '//select[starts-with(@id, "SelectedSchedule")]'
    SELECT_ALTERNATE_MODEL = LOCATION + '//select[starts-with(@id, "AlternateModel")]'

    def __init__(self, driver: WebDriver, order: TruckOrder):
        """
        :param WebDriver driver: Selenium Web Driver object
        :param TruckOrder order: Truck order
        """

        super().__init__(driver)
        self.order = order

    def verify_data(self, data: str) -> None:
        """
        Select verification of specific data

        :param str data: item to verify on the page
        """

        verification_map = {
            'price': self.verify_items_price,
            'size': self.verify_items_size
        }
        verification_map[data.lower()]()

    def verify_items_size(self) -> None:
        """
        Verifies the selected size of all trucks on the page
        """

        items_size = [size.text.strip().lower() for size in self.find_elements(self.TRUCK_SIZE)]
        assert all(size.startswith(self.order.truck_size.lower()) for size in items_size), \
            f"Some items have incorrect size:\nExpected: {self.order.truck_size}\nActual: {items_size}"

    def verify_items_price(self) -> None:
        """
        Verifies the selected price of all trucks on the page
        """

        items_price = [float(price.text.lower().replace('$', '').split()[0])
                       for price in self.find_elements(self.TRUCK_PRICE)]
        assert all(price == self.order.truck_price_records['rate'] for price in items_price), \
            f"Some items have incorrect price:\nExpected: {self.order.truck_size}\nActual: {items_price}"

    def select_closest_truck(self) -> None:
        """
        Selects the closest available truck
        """

        self.find_element(self.CONTINUE.format('Available and Closest')).click()
        sleep(1)

    def select_dropdown_option(self, dropdown_label: str) -> None:
        """
        Selects a dropdown value
        """

        select = Select(self.find_element(getattr(self, f"SELECT_{dropdown_label}").format(self.order.truck_size)))
        select.select_by_visible_text(self.order.pick_up_time)