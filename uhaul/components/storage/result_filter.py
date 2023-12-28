from selenium.webdriver.common.by import By

from base.components.base import Base


class ResultFilter(Base):
    """Works with the left filter on the Storage results page"""

    FILTER = '//div[@id="resultFilters"]'
    SECTION = FILTER + '//fieldset[./ul][contains(., "{}")]'
    OPTION = '//label[contains(., "{}")]'

    def verify_checked_options(self, **kwargs: str):
        """Verifies that checks from the Hero for are present in filter

        :param str kwargs: field: option to verify that checked
        """

        unchecked = []
        for k, v in kwargs.items():
            option = self.find_element(self.SECTION.format(k) + self.OPTION.format(v))
            try:
                input = option.find_element(By.XPATH, './input')
                assert input.get_attribute('checked')
            except AssertionError:
                unchecked.append({k: v})

        if unchecked:
            raise AssertionError(f'These options are not checked:\n{unchecked}')
