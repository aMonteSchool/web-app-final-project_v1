from datetime import date
from typing import Type
from dateutil import parser
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from uhaul.components.order_models.storage_order import StorageOrder
from uhaul.components.order_models.truck_order import TruckOrder
from uhaul.components.trucks.order_option import OrderOption


class StorageUnitsOption(OrderOption):
    STORAGES = '//div[contains(@id,"showcase")]//li[@class="cell"]'
    A_STORAGE = STORAGES + '//h4[contains(text(), "{unit_size}")]'
    STORAGE_PRICE = A_STORAGE + ('/parent::div[@class="cell auto"]/following-sibling::'
                                 'div//dl[contains(@class,"text-right")]//b')
    RENT_NOW_BUTTON = A_STORAGE + '/ancestor::div[@class="grid-x grid-full"]//label[contains(@class, "button-rentnow")]'
    CALENDAR_OPEN = A_STORAGE + ('/ancestor::div[@class="grid-x grid-full"]'
                                 '//div[contains(@id, "rentNowContainer")]//input[@name="MoveInDate"]')
    CALENDAR_MODAL = '//div[@id="ui-datepicker-div"]'
    CALENDAR_PAGE = '//div[contains(@id, "ui-datepicker")]'
    DATE = '//a[@class="ui-state-default"][@data-date="{day}"]'
    ADD_BUTTON = A_STORAGE + ('/ancestor::div[@class="grid-x grid-full"]'
                              '//div[contains(@id, "rentNowContainer")]//button[contains(text(), "Add to Cart")]')
    CONTINUE_BUTTON = '//button[contains(text(), "Continue")]'
    INSURANCE = '//ul[@class="storage-insurance-choice no-bullet"]//span[contains(text(), "{insurance}")]'
    INSURANCE_PRICE = INSURANCE + '/ancestor::div[@class="cell medium-auto"]/following-sibling::div//strong'

    def __init__(self, driver: WebDriver, order: Type[TruckOrder | StorageOrder] = None):
        super().__init__(driver)
        self.order = order

    def add_option(self, options):
        for k, v in options.items():
            option = {k: v}
            self.order.set_data(option)

        #  add storage unit price to truck price record
        self.collect_price()

        #  click "Rent Now" button
        self.find_element(self.RENT_NOW_BUTTON.format(unit_size=self.order.unit_size)).click()

        #  pick move-in date
        self.pick_date()

        #  click "Add to Cart" button
        self.find_element(self.ADD_BUTTON.format(unit_size=self.order.unit_size)).click()

        #  add insurance price to truck price record
        self.collect_insurance_price()

        #  click "Continue" button
        self.find_element(self.CONTINUE_BUTTON).click()

    def collect_price(self):
        price = float(
            self.find_element(self.STORAGE_PRICE.format(unit_size=self.order.unit_size)).text.replace('$', ''))

        self.order.truck_price_records |= {"storage_unit": price}

    def pick_date(self):
        """
        Picks a date of move-in
        """
        move_in_date = parser.parse(self.order.move_in_date).date()
        assert move_in_date >= date.today(), "Move-in date could not be in the past"
        self.find_element(self.CALENDAR_OPEN.format(unit_size=self.order.unit_size)).click()
        self.find_element(self.CALENDAR_MODAL)

        try:
            date_page = self.find_element(
                self.CALENDAR_PAGE.format(month=move_in_date.strftime("%B"), year=move_in_date.strftime("%Y")),
                timeout=3)
            date_page.find_element(By.XPATH, f".{self.DATE.format(day=move_in_date.day+2)}").click()
        except ValueError:
            raise ValueError("Select the move-in date within 7 days")

    def collect_insurance_price(self):
        property_insurance = f"{float(self.order.property_insurance):,.0f}"

        price_text = self.find_element(self.INSURANCE_PRICE.format(insurance=property_insurance)).text

        #  clean text from "$##.## per month" to float
        price = float(''.join(char for char in price_text if char.isdigit() or char == '.'))

        self.order.truck_price_records |= {"insurance": price}
