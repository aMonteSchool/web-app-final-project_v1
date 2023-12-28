from github.components.element_base import ElementBase


class Followers(ElementBase):
    def __init__(self, driver):
        super().__init__(driver)
        self.FOLLOWERS = f"//div[@class='followers']/article"
        self.MAX = 100

    def get_path_pair(self, label):
        """
        return (xpath, json_path) by label
        """

        map = {
            'usernames': (f"{self.FOLLOWERS}//h4", "$..login"),
            'links': (f"{self.FOLLOWERS}//a", "$..html_url"),
        }

        value = map.get(label)
        if not value:
            raise ValueError(f'No key {label} exist')

        return value

    def get_followers_elements(self):
        return self.get_elements_by_xpath(self.FOLLOWERS)
