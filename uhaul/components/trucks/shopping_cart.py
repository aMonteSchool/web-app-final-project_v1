from selenium.webdriver.chrome.webdriver import WebDriver

from uhaul.components.order_models.bike_racks_order import BikeRacksOrder
from uhaul.components.order_models.storage_order import StorageOrder
from uhaul.components.order_models.truck_order import TruckOrder
from uhaul.components.order_models.ubox_order import UboxOrder
from uhaul.components.trucks.table import Table


class ShoppingCart(Table):
    CART_TABLE = '//div[@id="UMoveComponent"]//table'
    DUE_TODAY = '//div[contains(@class, "divider")][.//dt[contains(., "Due Today")]]//dd'
    DUE_AT_PICKUP = ('//div[contains(@class, "secondary")]'
                     '//dt[contains(., "Equipment Rental")]/following-sibling::dd[position() = 1]')
    ENVIRONMENTAL_FEE = ('//table[contains(@class, "cart")]'
                         '//td[contains(., "Environmental")]/following-sibling::td[@class="text-right"]')
    VEHICLE_LICENSE_RECOVERY = ('//table[contains(@class, "cart")]'
                         '//td[contains(., "License")]/following-sibling::td[@class="text-right"]')

    MOVING_FEE = '//div[@id="MovingHelpComponent"]//td[contains(text(),"Handling Fee")]/ancestor::tr//td[contains(@class, "text-right")]'

    SUBTOTAL = '//th[contains(text(), "Subtotal")]//ancestor::tr//td[contains(@class, "text-right")]'

    def __init__(self, driver: WebDriver, order: TruckOrder | StorageOrder | BikeRacksOrder | UboxOrder ):
        super().__init__(driver)
        self.order = order


    def verify_price_self_storage(self):
        actual_price = float(self.find_element(self.DUE_TODAY).text.replace('$', '').split('\n')[0])

        expected_price = round(sum(self.order.storage_price_records.values()), 2)


        assert actual_price == expected_price, (f"Self storage price is not as expected:"
                                                f"\nExpected: {expected_price}"
                                                f"\nActual: {actual_price}")


    def verify_price_bike_rack(self):
        actual_price = float(self.find_element(self.DUE_TODAY).text.replace('$', '').split('\n')[0])

        expected_price = round(sum(self.order.bike_racks_price_records.values()), 2)

        assert actual_price == expected_price, (f"Bike rack price is not as expected:"
                                                f"\nExpected: {expected_price}"
                                                f"\nActual: {actual_price}")


    def verify_price_due_at_pickup(self):
        due_pickup = float(self.find_element(self.DUE_AT_PICKUP).text.replace('$', '').split('\n')[0])
        due_today = float(self.find_element(self.DUE_TODAY).text.replace('$', '').split('\n')[0])
        actual_price = due_today + due_pickup
        #  Round expected price to two decimal places to avoid floating point calculation problem
        expected_price = round(sum(self.order.truck_price_records.values()), 2)
        # expected_price = sum(self.order.truck_price_records.values())
        # self.make_screenshot('price_validation_screenshot.png')

        assert actual_price == expected_price, (f"Due at Pick Up price is not as expected:"
                                                f"\nExpected: {expected_price}"
                                                f"\nActual: {actual_price}")

    def verify_ubox_order_price(self):
        subtotal = float(self.find_element(self.SUBTOTAL).text.replace('$', '').split('\n')[0])
        actual_price = subtotal
        #  Round expected price to two decimal places to avoid floating point calculation problem
        expected_price = round(sum(self.order.ubox_price_records.values()), 2)
        # expected_price = sum(self.order.truck_price_records.values())
        # self.make_screenshot('price_validation_screenshot.png')

        assert actual_price == expected_price, (f"UBox order price is not as expected:"
                                                f"\nExpected: {expected_price}"
                                                f"\nActual: {actual_price}")


    def collect_environmental_fee(self):
        price = float(self.find_element(self.ENVIRONMENTAL_FEE.format(size=self.order.truck_size)).text.replace('$', ''))

        self.order.truck_price_records |= {"environmental": price}


    def collect_vehicle_license_recovery(self):
        price = float(
            self.find_element(self.VEHICLE_LICENSE_RECOVERY).text.replace('$', ''))

        self.order.truck_price_records |= {"vehicle_licence_recovery": price}


    def collect_moving_fee(self):
        try:
            price = float(
                self.find_element(self.MOVING_FEE).text.replace('$', ''))

            self.order.truck_price_records |= {"moving_fee": price}
        except(Exception):
            print("Moving help was not selected")

