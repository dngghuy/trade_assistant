from trade_assistant.model.abstract import AbstractModel
from trade_assistant.model.order import Order
from trade_assistant.model.consts import OrderType


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
        self.wealth_history = []

    def update(self, order: Order):
        """
        Currently, accepts the order iteratively, and update when the order is filled
        When strategy decide to make order, it should execute so that the call does not exceed the cash.
        """
        total_amount = order.quantity * order.price
        ticker = order.symbol
        if order.order_type in [
            OrderType.TYPE_SELL_LIMIT.value,
            OrderType.TYPE_SELL_MARKET.value,
            OrderType.TYPE_TAKE_PROFIT.value,
            OrderType.TYPE_TAKE_PROFIT_LIMIT.value,
            OrderType.TYPE_STOP_LOSS.value,
            OrderType.TYPE_STOP_LOSS_LIMIT.value
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

    def _check_if_bid_feasible(self, order: Order):
        """
        Check whether the amount of money is enough to make the bid order
        :param order:
        :return:
        """
        total_cash_order = order.quantity * order.price
        if total_cash_order > self.current_asset['cash']:
            return False
        return True

    def _check_if_ask_feasible(self, order: Order):
        """
        Check whether the amount of stock is enough to make the ask order
        :param order:
        :return:
        """
        current_asset_hold = self.current_asset[order.symbol]
        if current_asset_hold < order.quantity:
            return False
        return True
