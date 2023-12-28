from github.components.element_base import ElementBase


class User(ElementBase):
    def __init__(self, driver):
        super().__init__(driver)

    def get_path_pair(self, label):
        """
        return (xpath, json_path) by label
        """

        map = {
            'name': ("//header//h4", "$.name"),
            'twitter': ("//header//p[contains(text(), '@')]", "$.twitter_username"),
            'bio': ("//p[@class='bio']", "$.bio"),
            'company': ("//div[@class='links']/p[1]", "$.company"),
            'location': ("//div[@class='links']/p[2]", "$.location"),
            'blog': ("//div[@class='links']/a", "$.blog"),
            'follow': ("//header//a[text()='follow']", "$.html_url"),
        }
        value = map.get(label)
        if not value:
            raise ValueError(f'No key {label} exist')

        return value

    def compute_blog(self, values):
        return [f"https://{value}/" for value in values]

    def compute_twitter(self, values):
        return [f"@{value}" for value in values]
