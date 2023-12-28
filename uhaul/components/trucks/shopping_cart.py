from selenium.webdriver.chrome.webdriver import WebDriver

from uhaul.components.order_models.truck_order import TruckOrder
from uhaul.components.trucks.table import Table


class ShoppingCart(Table):
    CART_TABLE = '//div[@id="UMoveComponent"]//table'
    DUE_TODAY = '//div[contains(@class, "divider")][.//dt[contains(., "Due Today")]]//dd'
    DUE_AT_PICKUP = ('//div[contains(@class, "secondary")]'
                     '//dt[contains(., "Equipment Rental")]/following-sibling::dd[position() = 1]')
    ENVIRONMENTAL_FEE = ('//table[contains(@class, "cart")]'
                         '//td[contains(., "Environmental")]/following-sibling::td[@class="text-right"]')

    def __init__(self, driver: WebDriver, order: TruckOrder):
        super().__init__(driver)
        self.order = order

    def verify_price_due_at_pickup(self):
        actual_price = float(self.find_element(self.DUE_AT_PICKUP).text.replace('$', '').split('\n')[0])

        #  Round expected price to two decimal places to avoid floating point calculation problem
        expected_price = round(sum(self.order.truck_price_records.values()), 2)
        expected_price = sum(self.order.truck_price_records.values())
        self.make_screenshot('price_validation_screenshot.png')

        assert actual_price == expected_price, (f"Due at Pick Up price is not as expected:"
                                                f"\nExpected: {expected_price}"
                                                f"\nActual: {actual_price}")

    def collect_environmental_fee(self):
        price = float(self.find_element(self.ENVIRONMENTAL_FEE.format(size=self.order.truck_size)).text.replace('$', ''))

        self.order.truck_price_records |= {"environmental": price}
