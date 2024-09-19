from typing import Optional, Dict
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from uhaul.components.order_models.truck_order import TruckOrder
from uhaul.components.trucks.order_option import OrderOption

class BoxesOption(OrderOption):

    ITEM = '//ul[@id="PickupProductList_suppliesList"]//div[contains(@class, "grid-full")]'
    PRODUCT_NAME = ITEM + '//a[contains(text(), "{item_name}")]'
    COUNT = ITEM + '//a[contains(text(), "{item_name}")]//..//..//input'
    PRICE = ITEM + '//a[contains(text(), "{item_name}")]//..//..//dd[contains(@class, "price")]'
    ADD_SUPPLIES_BUTTON = '//button[@id="btnAddSupplies"]'
    TOTAL_PRICE = '//span[@id="pretaxSubTotal"]'


    def __init__(self, driver: WebDriver, order: TruckOrder = None):
        super().__init__(driver)
        self.order = order

    def add_option(self, options: Optional[Dict[str, str]] = None):
        for key, value in options.items():
            self.find_element(self.COUNT.format(item_name=key)).clear()
            self.find_element(self.COUNT.format(item_name=key)).send_keys(value)

        self.find_element(self.TOTAL_PRICE).click()
        #  add storage unit price to truck price record
        self.collect_price()

        #  click 'Add supplies' button
        self.find_element(self.ADD_SUPPLIES_BUTTON).click()
        WebDriverWait(self.driver, 10).until(ec.invisibility_of_element((By.XPATH, self.ADD_SUPPLIES_BUTTON)))


    def collect_price(self):
        total_price = float(self.find_element(self.TOTAL_PRICE).text)
        self.order.truck_price_records |= {'boxes': total_price}