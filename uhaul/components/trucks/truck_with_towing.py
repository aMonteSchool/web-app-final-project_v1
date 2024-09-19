
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from base.components.base import Base
from selenium.webdriver.common.by import By
from uhaul.components.order_models.truck_order import TruckOrder
from selenium.webdriver.support.ui import Select


class TruckWithTowing(Base):
    TRUCK_WITH_TOWING = '//a[contains(@href, "RatesTowingCombo")]'
    VEHICLE_YEAR = '//select[@id = "Year_ValueTowed"]'
    VEHICLE_MAKE = '//select[@id = "Make_ValueTowed"]'
    VEHICLE_MODEL = '//select[@id = "VehicleModel_ValueTowed"]'
    VEHICLE_FEATURE = '//select[@id = "Features_ValueTowed"]'
    WILL_IT_WORK_BUTTON = '//button[@id = "btnShowTowing"]'
    PRICE = '//b[@id = "subtotal"]'
    CONTINUE_BUTTON = '//button[@id = "btnSelectProcessRequest"]'

    def __init__(self, driver: WebDriver, order: TruckOrder):
        super().__init__(driver)
        self.order = order
        self.sizes = ['Small', '8', '9', '10', '15', '17', '20', '26']

    def select_truck_with_towing(self, options):
        for k, v in options.items():
            option = {k: v}
            self.order.set_data(option)

        self.find_element(self.TRUCK_WITH_TOWING).click()

        Select(self.find_element(self.VEHICLE_YEAR)).select_by_visible_text(self.order.towing_year)

        WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable((By.XPATH, self.VEHICLE_MAKE)))
        Select(self.find_element(self.VEHICLE_MAKE)).select_by_visible_text(self.order.towing_make)

        WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable((By.XPATH, self.VEHICLE_MODEL)))
        Select(self.find_element(self.VEHICLE_MODEL)).select_by_visible_text(self.order.towing_model)

        WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable((By.XPATH, self.VEHICLE_FEATURE)))
        Select(self.find_element(self.VEHICLE_FEATURE)).select_by_visible_text(self.order.towing_feature)

        self.find_element(self.WILL_IT_WORK_BUTTON).click()

        self.collect_price()

        self.find_element(self.CONTINUE_BUTTON).click()

    def collect_price(self):
        price = float(self.find_element(self.PRICE.format(size=self.order.truck_size)).text.replace('$', ''))

        self.order.truck_price_records |= {"rate": price}
