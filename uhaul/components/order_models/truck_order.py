from uhaul.components.order_models.order import Order


class TruckOrder(Order):
    """Truck Order Model"""

    def __init__(self):
        self.pick_up_location: str = '08816'
        self.pick_up_city: str = 'East Brunswick, NJ'
        self.pick_up_address: str = '59 Ranger Rd'
        self.drop_off_location: str = '08816'
        self.pick_up_date: str = '10.17.2024'
        self.pick_up_time: str = '10:00 AM'
        self.truck_size: str = '15'
        self.truck_price_records: dict = {}
        self.truck_size: str = '15'
        self.coverage: str = 'Safemove'
        self.unit_size: str = 'Medium'
        self.move_in_date: str = '09.01.2024'
        self.property_insurance: str = '5000'
        self.moving_type: str = 'Loading'
        self.moving_provider: str = 'Moving Hard'
        self.load_unload_date = '09.01.2024'
        self.start_time = 'Morning'
        self.towing_year = '2018'
        self.towing_make = 'BMW'
        self.towing_model = '320i'
        self.towing_feature = 'Rear Wheel Drive'
