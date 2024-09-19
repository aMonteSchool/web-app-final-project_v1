import time
from selenium.webdriver.chrome.webdriver import WebDriver
from uhaul.components.order_models.bike_racks_order import BikeRacksOrder
from uhaul.components.trucks.order_option import OrderOption


class BikeRacks(OrderOption):
    HEADER_TEXT = 'Bike Racks'

    FILTER = '//label[contains(text(),"{filter_name}")]/div[contains(@class, "custom-dropdown-area")]'
    FILTER_BUTTON = FILTER + '/button'
    FILTER_ITEM = FILTER + '//child::a[contains(text(), "{filter_value} ")]'
    RESET_FILTER_BUTTON = '//button[@id="bikeRacksClearFilters"]'
    FILTER_MAP = {
        'No. of Bikes': 'Filter_NumberOfBikes_container',
        'Brand': 'Filter_Brand_container',
        'Rack Type': 'Filter_HitchReceiverSize_container',
        'Features': 'Filter_Features_container'
    }

    DRAWER_MENU_BUTTON = '//button[@id="mobileMenuBtn"]'
    MAIN_MENU = '//li[@class="cell large-shrink"][./a[contains(text(), "{menu}")]]'
    MENU_ITEM = '//a[contains(text(),"{option}")]'

    RESULTS_HEADER = '//h3//span[@class="uhjs-br-results-text"]'
    SEE_MORE_BUTTON = '//button[@class="clear link"]'
    ITEMS_SMALL = '//div[@class="show-for-small-only"]//child::li'
    ITEMS_MEDIUM = '//div[@class="show-for-medium"]//child::li'

    BIKE_RACK = '//b[contains(text(), "{name}")]'
    PRICE = '//b[contains(text(), "{name}")]/ancestor::div[contains(@class, "medium-text")]//p[contains(@class, "text-dark")]/b'

    ADD_TO_CART = '//button[@id = "addToCart"]'
    VIEW_CART = '//a[@id = "viewCart"]'
    SHIP_TO_ME_OPTION = '//input[@id = "shipToMe"]/ancestor::li'

    def __init__(self, driver: WebDriver, order: BikeRacksOrder = None):
        super().__init__(driver)
        self.order = order

    def verify_header(self):
        header_text = self.find_element('//h1').text
        assert header_text == self.HEADER_TEXT, (f"Page header is not as expected:"
                                                 f"\nExpected: {self.HEADER_TEXT}"
                                                 f"\nActual: {header_text}")

    def set_rack_filter(self, filter_options):
        # Reset Filter
        self.click(self.RESET_FILTER_BUTTON)

        # Set Filter
        for key, value in filter_options.items():
            self.action_click(self.FILTER.format(filter_name=key))
            time.sleep(0.5)
            self.action_click(self.FILTER_ITEM.format(filter_name=key, filter_value=value))
            self.action_click(self.FILTER.format(filter_name=key))

    def select_menu(self, menu, option):
        menu_xpath = self.MAIN_MENU.format(menu=menu)
        menu_item_xpath = self.MENU_ITEM.format(option=option)
        if self.find_element(self.DRAWER_MENU_BUTTON):
            self.click(self.DRAWER_MENU_BUTTON)
            self.click(menu_xpath)
        self.click(menu_item_xpath)

    def verify_number(self):
        if self.find_element(self.SEE_MORE_BUTTON):
            self.click(self.SEE_MORE_BUTTON)
        expected_results = self.find_element(self.RESULTS_HEADER).text.split(' ')[0]
        # if self.find_element(self.ITEMS_SMALL):
        #     items = self.find_elements(self.ITEMS_SMALL)
        # else:
        items = self.find_elements(self.ITEMS_MEDIUM)
        item_list = []
        item_list.extend(i for i in items)
        actual_result = str(len(item_list))
        assert expected_results == actual_result, (f"Results number is not as expected:"
                                                   f"\nExpected: {expected_results}"
                                                   f"\nActual: {actual_result}")

    def select_bike_rack(self, options):
        for k, v in options.items():
            option = {k: v}
            self.order.set_data(option)

        self.collect_price()
        self.find_element(self.BIKE_RACK.format(name=self.order.bike_rack)).click()


    def click_add_to_card(self):
        self.find_element(self.ADD_TO_CART).click()


    def click_vew_cart(self):
        self.find_element(self.VIEW_CART).click()


    def select_ship_to_me_option(self):
        self.find_element(self.SHIP_TO_ME_OPTION).click()


    def collect_price(self):
        price = float(self.find_element(self.PRICE.format(name=self.order.bike_rack)).text.replace('$', ''))

        self.order.bike_racks_price_records |= {"rate": price}


