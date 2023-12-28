from selenium.webdriver.chrome.webdriver import WebDriver

from base.components.base import Base


class Modal(Base):
    MODAL = '//div[contains(@id, "Modal")][contains(@style, "display: block;")]'
    CLOSE_MODAL = MODAL + '//button[@aria-label="Close Modal"]'

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def close_modal(self):
        self.find_element(self.CLOSE_MODAL).click()