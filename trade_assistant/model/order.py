from trade_assistant.model.abstract import AbstractModel
from trade_assistant.model.consts import OrderStatus, OrderType


class Order(AbstractModel):
    resource_name: str = 'orders'
    order_type: str = OrderType.TYPE_BUY_LIMIT.value
    symbol: str = ''
    currency: str = ''
    quantity: float = 0
    test: bool = False
    price: float = 0
    status: OrderStatus = OrderStatus.NEW

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_status(self, status: OrderStatus):
        self.status = status

