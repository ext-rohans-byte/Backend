from dataclasses import dataclass
from typing import List

@dataclass
class OrderItemData:
    product_id: int
    quantity: int

@dataclass
class CreateOrderData:
    items: List[OrderItemData]
    address: str
    pincode: str