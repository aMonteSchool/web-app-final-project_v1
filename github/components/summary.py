from github.components.element_base import ElementBase


class Summary(ElementBase):
    def __init__(self, driver):
        super().__init__(driver)

    def get_path_pair(self, label):
        """
        return (xpath, json_path) by label
        """

        SUMMARY = f"//article[@class='item'][.//text()='{label}']//preceding-sibling::h3"

        path_map = {
            # summary
            'repos': (SUMMARY, "$.public_repos"),
            'followers': (SUMMARY, "$.followers"),
            'following': (SUMMARY, "$.following"),
            'gists': (SUMMARY, "$.public_gists")
        }
        value = path_map.get(label)
        if not value:
            raise ValueError(f'No key {label} exist')

        return value
