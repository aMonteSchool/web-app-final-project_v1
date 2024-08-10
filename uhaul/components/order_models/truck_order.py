from uhaul.components.order_models.order import Order


class TruckOrder(Order):
    """Truck Order Model"""

    def __init__(self):
        self.pick_up_location: str = '08816'
        self.pick_up_city: str = 'East Brunswick, NJ'
        self.drop_off_location: str = '08816'
        self.pick_up_date: str = '08.17.2024'
        self.pick_up_time: str = '10:00 AM'
        self.truck_size: str = '15'
        self.truck_price_records: dict = {}
        self.truck_size: str = '15'
        self.coverage: str = 'Safemove'
        self.unit_size: str = 'Medium'
        self.move_in_date: str = '09.01.2024'
        self.property_insurance: str = '5000'
