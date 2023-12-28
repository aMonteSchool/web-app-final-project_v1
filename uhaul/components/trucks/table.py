from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from base.components.base import Base


class Table(Base):
    TABLE = '//table'
    HEADERS = TABLE + '//th'
    ROWS = TABLE + '/*[self::tbody or self::tfoot]/tr[not(contains(@class, "hide"))]'

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.table = self.__table()
        self.headers = self.__collect_headers()
        self.records = self.collect_records()

    def __table(self):
        return self.find_element(self.TABLE)

    def __collect_headers(self):
        return [header.text.lower().strip() for header in self.find_elements(self.HEADERS, status='Presence')]

    def collect_records(self):
        records = []
        for row in self.__collect_rows()[1:]:
            cells = [cell.text for cell in row.find_elements(By.XPATH, './/td') if cell.text]
            records.append(dict(zip(self.headers, cells)))

        return records

    def __collect_rows(self):
        return self.find_elements(self.ROWS)
