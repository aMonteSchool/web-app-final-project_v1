from time import sleep

from selenium.webdriver.chrome.webdriver import WebDriver
from uhaul.components.order_models.ubox_order import UboxOrder
from uhaul.components.trucks.order_option import OrderOption
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from dateutil import parser


class UBoxOption(OrderOption):

    # page 1
    MOVING_FROM = '//input[@id = "PickupLocation-UBox"]'
    MOVING_TO = '//input[@id = "DropoffLocation"]'

    LOADING_DATE = '//input[@id = "PickupDate" or @id = "OriginDate"]'
    CALENDAR_MODAL = '//div[@id="ui-datepicker-div"]'
    CALENDAR_PAGE = '//div[contains(@id, "ui-datepicker")]'
    DATE_PICKER = '//a[@class="ui-state-default"][@data-date="{day}"]'

    GET_RATES_BUTTON = '//button[@type = "submit" and @class = "expanded"]'

    # page 2
    CONTAINERS_COUNT = '//select[@id = "selectNumBoxes"]'
    PRICE = '//span[@id = "uboxEstimateOneway"]'
    CONTINUE_BUTTON = '//button[@id = "btnContinue"]'

    # page 3
    ADDRESS = '//input[@id = "OriginAddress"]'
    CITY = '//input[@id = "OriginCity" and @type = "text"]'
    STATE = '//input[@id = "OriginState" and @type = "text"]'
    ZIP_CODE = '//input[@id="OriginPostalCode"]'
    ESTIMATE_BUTTON = '//button[@id = "btnEstimate"]'


    # page 4
    SELECT_BUTTON = '//h3[contains(text(), "{delivery_option}")]/ancestor::div[contains(@class, "medium-auto")]//button[@id = "selectBtnMore"]'
    DELIVERY_PRICE = '//h3[contains(text(), "{delivery_option}")]/ancestor::div[contains(@class, "medium-auto")]//span[contains(@class, "text")]'
    TRUCK_PICKUP_DATE = '//input[@id = "SelectedTruckPickupDate"]'
    DELIVERY_CONTINUE_BUTTON = '//button[@id = "btnTruckSubmit"]'


    # page 5
    OPEN_DROPDOWN = '//button[contains(@class, "dropdown")]'
    SELECT_COVERAGE = '//strong[contains(text(), "{coverage}")]'
    SELECT_COVERAGE_BUTTON = '//button[@id = "buttonSelectCoverage"]'

    def __init__(self, driver: WebDriver, order: UboxOrder = None):
        super().__init__(driver)
        self.order = order

    def get_ranked_container_rates(self, options):
        for k, v in options.items():
            option = {k: v}
            self.order.set_data(option)

        self.find_element(self.MOVING_FROM).send_keys(self.order.moving_from)

        self.select_loading_date()

        self.find_element(self.GET_RATES_BUTTON).click()

        # WebDriverWait(self.driver, 10).until(ec.invisibility_of_element((By.XPATH, self.CONFIRM_LOCATION)))


    def select_loading_date(self):
       self.set_date(self.LOADING_DATE,  parser.parse(self.order.loading_date).date())


    def set_date(self, locator, date):
        self.find_element(locator).click()

        date_page = self.find_element(self.CALENDAR_PAGE, timeout=3)
        date_page.find_element(By.XPATH, f".{self.DATE_PICKER.format(day=date.day)}").click()


    def select_containers_count(self, containers_count):
        if containers_count == 1:
            text = f"{containers_count} Container"
        else:
            text = f"{containers_count} Containers"

        Select(self.find_element(self.CONTAINERS_COUNT)).select_by_visible_text(text)
        sleep(1)
        self.collect_container_price()
        self.find_element(self.CONTINUE_BUTTON).click()


    def collect_container_price(self):
        price_text = self.find_element(self.PRICE).text

        #  clean text from "$##.## per month" to float
        price = float(''.join(char for char in price_text if char.isdigit() or char == '.'))

        self.order.ubox_price_records |= {"container_price": price}


    def plan_ubox_move(self, options):
        for k, v in options.items():
            option = {k: v}
            self.order.set_data(option)

        self.find_element(self.ADDRESS).send_keys(self.order.street_address)

        self.find_element(self.CITY).clear()
        self.find_element(self.CITY).send_keys(self.order.city)

        self.find_element(self.STATE).clear()
        self.find_element(self.STATE).send_keys(self.order.state)

        self.find_element(self.ZIP_CODE).clear()
        self.find_element(self.ZIP_CODE).send_keys(self.order.moving_from)

        self.find_element(self.ESTIMATE_BUTTON).click()


    def set_pickup_date(self):
        self.set_date(self.TRUCK_PICKUP_DATE, parser.parse(self.order.loading_date).date() + timedelta(days = 1))


    def collect_delivery_price(self):
        price_text = self.find_element(self.DELIVERY_PRICE.format(delivery_option=self.order.delivery_option)).text

        #  clean text from "$##.## per month" to float
        price = float(''.join(char for char in price_text if char.isdigit() or char == '.'))

        self.order.ubox_price_records |= {"delivery_price": price}


    def select_delivery_option(self, options):
        for k, v in options.items():
            option = {k: v}
            self.order.set_data(option)

        self.find_element(self.SELECT_BUTTON.format(delivery_option=self.order.delivery_option)).click()
        self.collect_delivery_price()
        self.set_pickup_date()
        self.find_element(self.DELIVERY_CONTINUE_BUTTON).click()


    def select_coverage(self, options):
        for k, v in options.items():
            option = {k: v}
            self.order.set_data(option)

        self.find_element(self.OPEN_DROPDOWN).click()
        self.find_element(self.SELECT_COVERAGE.format(coverage=self.order.coverage)).click()
        self.find_element(self.SELECT_COVERAGE_BUTTON).click()
