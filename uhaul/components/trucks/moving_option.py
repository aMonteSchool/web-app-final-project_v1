from selenium.webdriver.chrome.webdriver import WebDriver
from uhaul.components.order_models.truck_order import TruckOrder
from uhaul.components.trucks.order_option import OrderOption
from datetime import date
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from dateutil import parser


class MovingOption(OrderOption):

    LOADING_TYPE = '//ul[@id="movingHelpSearchServices"]//li[contains(@id, "{moving_type}")]'
    SELECT_LOADING_PROVIDER = '//*[contains(text(), "{provider_name}")]/ancestor::li[contains(@id, "MovingHelpProviders")]//button[contains(@id, "AddToCart")]'
    DATE = '//input[@id="ServiceDate"]'
    DATE_PICKER = '//a[@class="ui-state-default"][@data-date="{day}"]'
    START_TIME = '//select[@id="PreferredTime"]'
    ADDRESS = '//input[@id="Address"]'
    APARTMENT = '//input[@id="Address2"]'
    CITY = '//input[@id="City"]'
    STATE = '//input[@id="StateProvince"]'
    ZIP_CODE = '//input[@id="Zipcode"]'
    CONFIRM_LOCATION = '//button[@id="btnConfirmLocation"]'
    CALENDAR_MODAL = '//div[@id="ui-datepicker-div"]'
    CALENDAR_PAGE = '//div[contains(@id, "ui-datepicker")]'
    MOVING_PRICE = '//*[contains(text(), "{provider_name}")]/ancestor::li[contains(@id, "MovingHelpProviders")]//dd'


    def __init__(self, driver: WebDriver, order: TruckOrder = None):
        super().__init__(driver)
        self.order = order

    def add_option(self, options):
        for k, v in options.items():
            option = {k: v}
            self.order.set_data(option)

        self.find_element(self.LOADING_TYPE.format(moving_type=self.order.moving_type)).click()

        self.collect_moving_price()
        self.find_element(self.SELECT_LOADING_PROVIDER.format(provider_name=self.order.moving_provider)).click()

        self.pick_date()
        self.select_start_time()

        self.find_element(self.ADDRESS).clear()
        self.find_element(self.ADDRESS).send_keys(self.order.pick_up_address)

        self.find_element(self.CITY).clear()
        self.find_element(self.CITY).send_keys(self.order.pick_up_city)

        self.find_element(self.ZIP_CODE).clear()
        self.find_element(self.ZIP_CODE).send_keys(self.order.pick_up_location)

        self.find_element(self.CONFIRM_LOCATION).click()
        WebDriverWait(self.driver, 10).until(ec.invisibility_of_element((By.XPATH, self.CONFIRM_LOCATION)))


    def pick_date(self):
        self.find_element(self.DATE).click()
        load_unload_date = parser.parse(self.order.load_unload_date).date()
        assert load_unload_date >= date.today(), "Move-in date could not be in the past"

        date_page = self.find_element(
            self.CALENDAR_PAGE.format(month=load_unload_date.strftime("%B"), year=load_unload_date.strftime("%Y")),
            timeout=3)
        date_page.find_element(By.XPATH, f".{self.DATE_PICKER.format(day=load_unload_date.day + 2)}").click()


    def select_start_time(self):
        Select(self.find_element(self.START_TIME)).select_by_visible_text(self.order.start_time)


    def collect_moving_price(self):
        price_text = self.find_element(self.MOVING_PRICE.format(provider_name=self.order.moving_provider)).text

        #  clean text from "$##.## per month" to float
        price = float(''.join(char for char in price_text if char.isdigit() or char == '.'))

        self.order.truck_price_records |= {"moving_price": price}

