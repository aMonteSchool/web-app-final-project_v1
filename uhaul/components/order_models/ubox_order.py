from uhaul.components.order_models.order import Order
from datetime import datetime


class UboxOrder(Order):
    """Ubox Order Model"""

    def __init__(self):
        self.ubox_price_records: dict = {}
        self.loading_date: str = datetime.today().strftime("mm.dd.yyyy")
        self.moving_from: str = "98125"
        self.street_address: str = "14041 15th Ave NE, 204A"
        self.city: str = "Seattle"
        self.state: str = "WA"
        self.delivery_option: str = "We Deliver"
        self.coverage: str = "Decline storage insurance coverage"