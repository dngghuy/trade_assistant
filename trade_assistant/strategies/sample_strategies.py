"""
Logic for a naive, time independent strategy
"""

import pandas as pd

from trade_assistant.model.strategy import Strategy
from trade_assistant.model.order import Order
from trade_assistant.model.asset import Asset
from trade_assistant.model.consts import OrderStatus, OrderType
from trade_assistant.model.symbol import Symbol
from trade_assistant.signal_processing.moving_average import MovingAverage
from trade_assistant.signal_processing.resistance_support import SupportResistanceIndicator
from trade_assistant.signal_processing.comparison import (
    is_reaching_support,
    is_reaching_resistance,
    is_under_moving_average,
    is_through_support,
    is_through_resistance,
    is_over_moving_average
)
from typing import Optional


class SimpleADAStrategy(Strategy):
    def __init__(
        self,
        name: str,
        strategy_id: str,
        asset: Asset,
        indicators: list
    ):
        super().__init__(name, strategy_id, asset)
        self.list_indicators = indicators

    def _symbol_screening(self):
        pass

    @staticmethod
    def _make_bid_ask_order(
        symbol: Symbol,
        quantity: float,
        bid_ask_type: OrderType,
        price: Optional[float] = None
    ) -> Order:
        """
        Decide entry symbol/ price/ amount
        :return:
        """
        return Order(
            symbol=symbol.symbol,
            currency=symbol.currency,
            quantity=quantity,
            price=symbol.current if price is None else price,
            order_type=bid_ask_type
        )

    def _bid_amount_decision(self):
        """
        Decide the bid amount given the current asset information
        For this strategy, for simplicity, 10% of the init asset's wealth.
        :return:
        """
        return self.asset.wealth * 0.1

    def process(self, ada_snapshot: pd.DataFrame, symbol: Symbol) -> Optional[Order]:
        """
        Process buy/ sell with single stock.
        For simplicity, work with one symbol only.
        For this ver let's stick with 5m
        """
        # Given market snapshot and symbol's current price, calculate the indicators
        support_resistance_finder = SupportResistanceIndicator(
            rolling_wave_length=200,
            num_clusters=6
        ).process(ada_snapshot)
        moving_average_200_price = MovingAverage(
            rolling_wave_length=200,
            col='close'
        ).process(ada_snapshot)
        # moving_average_50_price = MovingAverage(
        #     rolling_wave_length=50,
        #     col='close'
        # ).process(ada_snapshot)
        moving_average_10_vol = MovingAverage(
            rolling_wave_length=10,
            col='volume'
        ).process(ada_snapshot)
        is_stock_reaching_support = is_reaching_support(
            support_resistance=support_resistance_finder.list_supports,
            prev_price=symbol,
            curr_price=symbol,
            thresh=0.1
        )
        is_stock_reaching_resistance = is_reaching_resistance(
            support_resistance=support_resistance_finder.list_resistances,
            prev_price=symbol,
            curr_price=symbol,
            thresh=0.1
        )
        is_stock_over_moving_average_200 = is_over_moving_average(
            moving_average=moving_average_200_price,
            price=symbol,
            compared_by='close'
        )
        is_stock_volume_over_moving_average_10 = is_over_moving_average(
            moving_average=moving_average_10_vol,
            price=symbol,
            compared_by='volume'
        )
        is_stock_volume_under_moving_average_10 = is_under_moving_average(
            moving_average=moving_average_10_vol,
            price=symbol,
            compared_by='volume'
        )
        # Case when stock is reaching support with large volume:
        if is_stock_reaching_support and is_stock_volume_over_moving_average_10:
            bid_amount = self._bid_amount_decision()
            order = self._make_bid_ask_order(
                symbol=symbol,
                quantity=bid_amount,
                bid_ask_type=OrderType.TYPE_BUY_LIMIT,
                price=symbol.current * (1 + 0.005)
            )
            return order
        # Case when stock is reaching support with large volume:
        elif is_stock_reaching_resistance and is_stock_volume_over_moving_average_10:
            bid_amount = self._bid_amount_decision()
            order = self._make_bid_ask_order(
                symbol=symbol,
                quantity=bid_amount,
                bid_ask_type=OrderType.TYPE_SELL_LIMIT,
                price=symbol.current * (1 - 0.005)
            )
            return order
        # Case when stock is reaching resistance but low volume
        elif is_stock_reaching_resistance and is_stock_volume_under_moving_average_10:
            bid_amount = self._bid_amount_decision()
            order = self._make_bid_ask_order(
                symbol=symbol,
                quantity=bid_amount,
                bid_ask_type=OrderType.TYPE_BUY_LIMIT,
            )
            return order
        # Case when stock is reaching support but low volume
        elif is_stock_reaching_support and is_stock_volume_under_moving_average_10:
            bid_amount = self._bid_amount_decision()
            order = self._make_bid_ask_order(
                symbol=symbol,
                quantity=bid_amount,
                bid_ask_type=OrderType.TYPE_SELL_LIMIT,
            )
            return order
        else:
            return None




