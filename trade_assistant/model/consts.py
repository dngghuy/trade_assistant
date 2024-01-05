from enum import Enum


class OrderStatus(Enum):
    NEW = 1
    PARTIALLY_FILLED = 2
    FILLED = 3
    CANCELED = 4
    REJECTED = 5


class OrderType(Enum):
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

