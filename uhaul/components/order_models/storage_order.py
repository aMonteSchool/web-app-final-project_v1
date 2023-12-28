from uhaul.components.order_models.order import Order
from typing import List


class StorageOrder(Order):
    """Storage Order Model"""

    def __init__(self):
        self.your_location: str = '33101'
        self.unit_size: List[str] = ['Small', 'Medium']
        self.types_of_storage: List[str] = ['Indoor Storage']
