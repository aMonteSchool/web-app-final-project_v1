from selenium.webdriver.chrome.webdriver import WebDriver

from base.components.base import Base
from uhaul.components.modal import Modal


class HowPickUp(Modal):
    MODAL = '//div[@id="sharedRevealContent"]'
    BUTTON_MOBILE = MODAL + '//button[contains(@id, "selfpickUp")]'
    BUTTON_COUNTER = MODAL + '//button[contains(@id, "counterPickUp")]'

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def select_option(self, option):
        self.find_element(getattr(self, f"BUTTON_{option}")).click()
