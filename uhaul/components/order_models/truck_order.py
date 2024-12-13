from uhaul.components.order_models.order import Order


class TruckOrder(Order):
    """Truck Order Model"""

    def __init__(self):
        self.pick_up_location: str = '80016'
        self.pick_up_city: str = 'Aurora, CO'
        self.drop_off_location: str = '80016'
        self.pick_up_date: str = '01.01.2025'
        self.pick_up_time: str = '10:00 AM'
        self.truck_size: str = "15' Truck"
        self.truck_price_records: dict = {}
        self.added_options: dict = {}
        self.coverage: str = 'Safemove'
        self.unit_size: str = 'Medium'
        self.move_in_date: str = '01.01.2025'
        self.property_insurance: str = '5000'
