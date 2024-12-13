from selenium.webdriver.chrome.webdriver import WebDriver
from datetime import datetime
from uhaul.components.order_models.truck_order import TruckOrder
from uhaul.components.trucks.table import Table


class ShoppingCart(Table):
    CART_TABLE = '//div[@id="UMoveComponent"]//table'
    DUE_TODAY = '//div[contains(@class, "divider")][.//dt[contains(., "Due Today")]]//dd'
    DUE_AT_PICKUP = ('//div[contains(@class, "secondary")]'
                     '//dt[contains(., "Equipment Rental")]/following-sibling::dd[position() = 1]')
    ENVIRONMENTAL_FEE = ('//table[contains(@class, "cart")]'
                         '//td[contains(., "ENVIRONMENTAL")]/following-sibling::td[@class="text-right"]')
    VEHICLE_RECOVERY_FEE = ('//table[contains(@class, "cart")]'
                            '//td[contains(., "Vehicle License Recovery Fee")]/following-sibling::td[@class="text-right"]')
    DATE_TIME = ('//table[contains(@class, "cart")]'
                 '//td[@class="show-for-medium" and contains(., "Scheduled Pickup")]')
    TRUCK_SIZE = ('//table[contains(@class, "cart")]'
                  '//td[@class="product-info"]/b')

    def __init__(self, driver: WebDriver, order: TruckOrder):
        super().__init__(driver)
        self.order = order

    def verify_price_due_at_pickup(self, options):
        actual_price = float(self.find_element(self.DUE_AT_PICKUP).text.replace('$', '').split('\n')[0])

        #  Round expected price to two decimal places to avoid floating point calculation problem
        expected_price = round(sum(self.order.truck_price_records.values()), 2)
        self.make_screenshot('price_validation_screenshot.png')

        assert actual_price == expected_price, (f"Due at Pick Up price is not as expected:"
                                                f"\nExpected: {expected_price}"
                                                f"\nActual: {actual_price}")

        for key, value in options.items():
            order_price = self.order.truck_price_records[key]
            order_amount = value
            actual_amount = self.find_element(
                '//tr[contains(., "' + key + '")]//td//select[@name="Quantity"]/option[@selected="selected"]').text
            actual_item_price = self.find_element('//tr[contains(., "' + key + '")]//td//b').text.replace('$', '')
            assert float(order_price) == float(actual_item_price), (
                f"Due at Pick Up price is not as expected for item " + key,
                f"\nExpected: {order_price}"
                f"\nActual: {actual_item_price}")
            assert order_amount == actual_amount, (f"Due at Pick Up amount is not as expected for item " + key,
                                                   f"\nExpected: {order_amount}"
                                                   f"\nActual: {actual_amount}")

    def collect_environmental_fee(self):
        price = float(
            self.find_element(self.ENVIRONMENTAL_FEE.format(size=self.order.truck_size)).text.replace('$', ''))

        self.order.truck_price_records |= {"environmental": price}

    def collect_vehicle_recovery_fee(self):
        price = float(
            self.find_element(self.VEHICLE_RECOVERY_FEE.format(size=self.order.truck_size)).text.replace('$', ''))

        self.order.truck_price_records |= {"vehicle_recovery": price}

    def make_screenshot(self, filename):
        self.driver.get_screenshot_as_file(filename)
        pass

    def verify_data(self, data: str) -> None:
        verification_map = {
            'time': self.verify_time,
            'date': self.verify_date,
            'truck size': self.verify_truck_size
        }
        verification_map[data.lower()]()

    def verify_time(self) -> None:
        element_text = self.find_elements(self.DATE_TIME)[0].text
        date_time = element_text.split('\n')[1]
        time_result = date_time.split('at')[-1].strip()
        assert self.order.pick_up_time.lower() == time_result.lower(), \
            f"The item has incorrect time:\nExpected: {self.order.pick_up_time}\nActual: {time_result}"

    def verify_date(self) -> None:
        element_text = self.find_elements(self.DATE_TIME)[0].text
        date_time = element_text.split('\n')[1]
        date_result = date_time.split('at')[0].strip()
        expected_date = datetime.strptime(self.order.pick_up_date, "%m.%d.%Y").strftime("%m/%#d/%Y").lstrip('0')
        actual_date = date_result
        assert expected_date == actual_date, \
            f"The item has incorrect date:\nExpected: {self.order.pick_up_date}\nActual: {date_result}"

    def verify_truck_size(self) -> None:
        actual_truck_size = self.find_elements(self.TRUCK_SIZE)[0].text
        expected_truck_size = self.order.truck_size
        assert expected_truck_size == actual_truck_size, \
            f"The item has incorrect truck size:\nExpected: {expected_truck_size}\nActual: {actual_truck_size}"
