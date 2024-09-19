from datetime import datetime
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from base.components.base import Base
from uhaul.components.order_models.storage_order import StorageOrder


class Storage(Base):
    VIEW_RATES_BUTTON = '//*[@id="storageResults"]//a[contains(text(), "{storage_name}")]/ancestor::li[@class = "divider"]//a[@class = "button "]'
    RENT_NOW_BUTTON = '//h4[contains(text(), "{unit_size}")]/ancestor::li[@class = "divider "]//li[contains(@class, "rent")]//a[@class = "button nowrap"]'
    SELECT_DATE = '//input[contains(@id , "MoveInDate") and  @required = "True"]'
    ADD_TO_CARD = '//button[@data-unit-movein-date]'
    CALENDAR_MODAL = '//div[@id="ui-datepicker-div"]'
    CALENDAR_PAGE = '//div[contains(@id, "ui-datepicker")]'
    DATE_PICKER = '//a[@class="ui-state-default"][@data-date="{day}"]'
    INSURANCE_TYPE = '//strong[contains(text(), "{insurance_type}")]'
    CONTINUE_BUTTON = '//button[@id = "storageInsuranceBtn"]'
    STORAGE_PRICE = '//h4[contains(text(), "{unit_size}")]/ancestor::li[@class = "divider "]//dd[@class = "text-small collapse"]/b'


    def __init__(self, driver: WebDriver, order: StorageOrder = None):
        super().__init__(driver)
        self.order = order


    def update_order(self, options):
        for k, v in options.items():
            option = {k: v}
            self.order.set_data(option)


    def select_storage(self, storage_name):
        self.update_order(storage_name)
        self.find_element(self.VIEW_RATES_BUTTON.format(storage_name=self.order.storage_name)).click()


    def select_storage_unit(self, storage_unit):
        self.update_order(storage_unit)
        self.collect_price()
        self.find_element(self.RENT_NOW_BUTTON.format(unit_size=self.order.storage_type)).click()
        self.select_date()
        self.find_element(self.ADD_TO_CARD).click()


    def select_insurance(self, insurance_type):
        self.update_order(insurance_type)
        self.find_element(self.INSURANCE_TYPE.format(insurance_type=self.order.insurance_type)).click()
        self.find_element(self.CONTINUE_BUTTON).click()


    def collect_price(self):
        price = float(self.find_element(self.STORAGE_PRICE.format(unit_size=self.order.storage_type)).text.replace('$', ''))

        self.order.storage_price_records |= {"storage_price": price}


    def select_date(self):
        self.find_element(self.SELECT_DATE).click()
        date = datetime.today()

        date_page = self.find_element(
            self.CALENDAR_PAGE.format(month=date.strftime("%B"), year=date.strftime("%Y")),
            timeout=3)
        date_page.find_element(By.XPATH, f".{self.DATE_PICKER.format(day=date.day + 2)}").click()




