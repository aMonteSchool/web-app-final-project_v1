class Order:
    """Order Model"""

    def set_data(self, data: dict):
        """Sets data for an order

        :param dict data: data to set in an order
        """

        if not data:
            return

        for k, v in data.items():
            if not hasattr(self, k):
                raise ValueError(f"No such attribute: {k}")

            setattr(self, k, v)