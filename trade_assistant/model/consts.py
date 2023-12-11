from enum import Enum


class OrderStatus(Enum):
    NEW = 1
    PARTIALLY_FILLED = 2
    FILLED = 3
    CANCELED = 4
    REJECTED = 5
