from .abstract import AbstractModel
from .consts import OrderStatus


class Order(AbstractModel):
    # limit: execute when reached
    TYPE_BUY_LIMIT: str = 'BUY_LIMIT'
    TYPE_SELL_LIMIT: str = 'SELL_LIMIT'
    # buy/sell immediately
    TYPE_BUY_MARKET: str = 'BUY_MARKET'
    TYPE_SELL_MARKET: str = 'SELL_MARKET'
    # Sell when the stop price is reached.
    TYPE_STOP_LOSS: str = 'STOP_LOSS'
    # Sell when at limit price when stop price is reached
    TYPE_STOP_LOSS_LIMIT: str = 'STOP_LOSS_LIMIT'
    # Take profit is order that allows you to set a target profit price.
    TYPE_TAKE_PROFIT: str = 'TAKE_PROFIT'
    # Take profit limit is an advanced order that creates a limit order when the stop price is reached.
    TYPE_TAKE_PROFIT_LIMIT: str = 'TAKE_PROFIT_LIMIT'
    TYPE_LIMIT_MAKER: str = 'LIMIT_MAKER'
    HOLD: str = 'HOLD'

    resource_name: str = 'orders'

    type: str = TYPE_BUY_LIMIT
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



