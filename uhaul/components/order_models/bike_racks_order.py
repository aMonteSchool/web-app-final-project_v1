from uhaul.components.order_models.order import Order


class BikeRacksOrder(Order):
    """Bike Order Model"""

    def __init__(self):
        #self.truck_size: str = '15'
        self.bike_racks_price_records: dict = {}
        self.bike_rack: str = "Swagman XC 2 Bike Rack"