from github.components.element_base import ElementBase


class Search(ElementBase):
    def __init__(self, driver):
        super().__init__(driver)

    def get_search_field(self):
        return self.get_element_by_xpath('//input[@data-testid="search-bar"]')

    def is_search_result(self):
        return len(self.get_elements_by_xpath('//section[@class="section"]')) > 1
