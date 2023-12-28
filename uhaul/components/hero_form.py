from time import sleep
from typing import List

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from base.components.base import Base
from base.components.calendar import PickupDate
from uhaul.components.order_models.storage_order import StorageOrder
from uhaul.components.order_models.truck_order import TruckOrder


class HeroForm(Base):
    """Works with Hero form on the home page"""

    TAB = '//*[@id="heroTabs"]//a[normalize-space(.) = "{tab}"]'
    BUTTON = '//div[contains(@class, "hero-tabs-content")]//button[contains(., "{}")]'
    FIELD_INPUT = '//input[parent::label[contains(., "{label}")]]'
    DROPDOWN_INPUT = '//div[@class = "selectbox"][preceding-sibling::legend[contains(normalize-space(.), "{label}")]]'
    DROPDOWN = '//div[@id][contains(@class, "selectbox-options open")]'
    DROPDOWN_CHECKBOX = '//label[contains(., "{option}")]'
    SELECTED_CONTAINER = '//div[contains(@id, "Container")]//div[contains(., "{option}")]'

    def __init__(self, driver: WebDriver, tab: str):
        """
        :param WebDriver driver: Selenium Web Driver object
        :param str tab: Tab to select on the form
        """

        super().__init__(driver)
        self.tab = tab
        self.click(self.TAB.format(tab=self.tab))
        button = 'Find Units' if tab == 'Storage Units' else 'Get Rates'
        self.BUTTON = self.BUTTON.format(button)

    def submit(self):
        self.click(self.BUTTON)

    def fill_form(self, order: TruckOrder | StorageOrder):
        """Selects the fields to fill out based on the tab

        :param TruckOrder | StorageOrder order: Order data to populate fields
        """

        form_map = {
            'Trucks & Trailers': self.fill_truck_form,
            'Storage Units': self.fill_storage_form
        }
        form_map[self.tab](order)
        self.submit()
        sleep(5)  # TODO: Convert into some explicit wait if needed

    def fill_field(self, label: str, option: str) -> None:
        """Populates desired field with the value

        :param str label: Label of the field to populate
        :param str option: Value to populate the field
        """

        field = self.find_element(self.FIELD_INPUT.format(label=label))
        self.send_keys(field, option)

    def fill_dropdown(self, label: str, options: List[str]) -> None:
        """Selects options in dropdown, verifies, closes

        :param str label:Label of the dropdown to select
        :param list options: List of options to select in dropdown
        """
        self.find_element(self.DROPDOWN_INPUT.format(label=label)).click()
        dd = self.find_element(self.DROPDOWN)

        option = None
        for option in options:
            dd.find_element(By.XPATH, self.DROPDOWN_CHECKBOX.format(option=option)).click()
            option = self.find_element(self.SELECTED_CONTAINER.format(option=option))

        self.click_by_offset(option, 50, 0)
        self.find_element(self.DROPDOWN, visibility=False)

    def fill_storage_form(self, order: StorageOrder) -> None:
        """ Fills out fields in Storage tab

        :param StorageOrder order: Order data to populate the form
        """

        self.fill_field("Your Location", order.your_location)

        self.fill_dropdown("Unit Size", order.unit_size)
        self.fill_dropdown("Types of Storage", order.types_of_storage)

    def fill_truck_form(self, order: TruckOrder) -> None:
        """Fills out fields in Truck tab

        :param TruckOrder order: Order data to populate the form
        """

        PickupDate(self.driver, order.pick_up_date).pick_date()

        self.fill_field("Pick Up Location", order.pick_up_location)
        self.fill_field("Drop Off Location", order.drop_off_location)
