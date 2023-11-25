from .abstract import AbstractModel


class Order(AbstractModel):
    BUY: str = 'BUY'
    SELL: str = 'SELL'
    TYPE_LIMIT: str = 'LIMIT'
    TYPE_MARKET: str = 'MARKET'
    TYPE_STOP_LOSS: str = 'STOP_LOSS'
    TYPE_STOP_LOSS_LIMIT: str = 'STOP_LOSS_LIMIT'
    TYPE_TAKE_PROFIT: str = 'TAKE_PROFIT'
    TYPE_TAKE_PROFIT_LIMIT: str = 'TAKE_PROFIT_LIMIT'
    TYPE_LIMIT_MAKER: str = 'LIMIT_MAKER'

    resource_name: str = 'orders'

    type: str = TYPE_LIMIT
    symbol: str = ''
    currency: str = ''
    asset: str = ''
    quantity: float = 0
    test: bool = False
    price: float = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
