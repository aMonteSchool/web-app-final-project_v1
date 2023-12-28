import time

from selenium.webdriver.chrome.webdriver import WebDriver

from base.components.base import Base


class OrderOption(Base):
    NO_THANKS = '//*[self::a or self::button][starts-with(normalize-space(.), "No thanks,")]'

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def skip_page(self):
        self.find_element(self.NO_THANKS)
        self.click(self.NO_THANKS)
