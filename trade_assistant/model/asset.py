from trade_assistant.model.abstract import AbstractModel
from trade_assistant.model.order import Order


class Asset(AbstractModel):
    """
    This object aims to manage the wealth of the bot
    """

    def __init__(self, asset_name: str, currency: str, init_wealth: float = 0, **kwargs):
        super().__init__(**kwargs)
        self.asset_name = asset_name
        self.currency = currency
        self.wealth = init_wealth
        self.current_asset = {
            'cash': init_wealth
        }

    def update(self, order: Order):
        """
        Currently, accepts the order iteratively, and update when the order is filled
        When strategy decide to make order, it should execute so that the call does not exceed the cash.
        """
        total_amount = order.quantity * order.price
        ticker = order.symbol
        if order.type in [
            Order.TYPE_SELL_LIMIT,
            Order.TYPE_SELL_MARKET,
            Order.TYPE_TAKE_PROFIT,
            Order.TYPE_TAKE_PROFIT_LIMIT,
            Order.TYPE_STOP_LOSS,
            Order.TYPE_STOP_LOSS_LIMIT
        ]:
            # Add to the current cash
            self.current_asset['cash'] += total_amount
            self.current_asset[ticker] -= order.quantity
            # If the symbol is zero, remove it from the current asset
            if self.current_asset[ticker] == 0:
                self.current_asset.pop(ticker)
        else:
            # Remove from the current cash
            self.current_asset['cash'] -= total_amount
            # Declare new or update the symbol
            if ticker not in self.current_asset:
                self.current_asset[ticker] = order.quantity
            else:
                self.current_asset[ticker] += order.quantity
