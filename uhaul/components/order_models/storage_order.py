from uhaul.components.order_models.order import Order
from typing import List


class StorageOrder(Order):
    """Storage Order Model"""

    def __init__(self):
        self.storage_price_records: dict = {}
        self.your_location: str = '33101'
        self.unit_size: List[str] = ['Small', 'Medium']
        self.types_of_storage: List[str] = ['Indoor Storage']
        self.insurance_type: str = "Use my homeowners/renters insurance"
        self.storage_name: str = "U-Haul Moving & Storage of Greater Miami"
        self.storage_type: str = "5' x 8' x 8'"
