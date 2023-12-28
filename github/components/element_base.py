from jsonpath_ng.ext import parse
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class ElementBase:
    def __init__(self, driver):
        self.driver = driver

    def get_path_pair(self, label):
        pass

    def get_element_by_xpath(self, xpath):
        try:
            return WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(
                (By.XPATH, xpath)))
        except TimeoutException:
            return None

    def get_elements_by_xpath(self, xpath):
        try:
            return WebDriverWait(self.driver, 5).until(EC.visibility_of_any_elements_located(
                (By.XPATH, xpath)))
        except TimeoutException:
            return None

    def get_elements_by_label(self, label):
        return self.get_elements_by_xpath(self.get_path_pair(label)[0])

    def get_elements_text_by_label(self, label):
        elements = self.get_elements_by_xpath(self.get_path_pair(label)[0])
        return self.get_text(elements)

    def get_elements_href_by_label(self, label):
        elements = self.get_elements_by_xpath(self.get_path_pair(label)[0])
        return self.get_href(elements)

    def get_href(self, web_elements):
        """
        :return: WebElement list
        """
        if web_elements:
            return [element.get_attribute('href').lower() for element in web_elements]
        return None

    def get_text(self, web_elements):
        """
        :return: WebElement list
        """
        if web_elements:
            values = []
            for element in web_elements:
                if not element.text:
                    return None
                values.append(element.text.lower())
            return values
        return None

    def eval_json_path_by_label(self, json, label):
        path = self.get_path_pair(label)[1]

        return self.eval_json_path_by_path(json, path)

    def eval_json_path_by_path(self, json, path):
        if path.startswith('$'):
            path_expression = parse(path)
            matches = path_expression.find(json)
            values = [str(match.value).lower() for match in matches]

            if values == ['none']:
                return None
            return values

    def get_button(self, text):
        return self.get_element_by_xpath(f'//button[text()="{text}"]')
