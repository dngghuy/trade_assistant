import pandas as pd

from trade_assistant.model.strategy import Strategy
from trade_assistant.model.order import Order
from trade_assistant.model.asset import Asset
from trade_assistant.model.consts import OrderStatus
from trade_assistant.model.price import Price
from trade_assistant.signal_processing.moving_average import MovingAverage
from trade_assistant.signal_processing.resistance_support import SupportResistanceIndicator


class SingleStockSamplePrice(Price):
    def __init__(
            self,
            pair: str,
            exchange: str,
            current: float,
            lowest: float,
            highest: float,
            currency: str,
            asset: str,
            volume: float
    ):
        super().__init__(
            pair=pair,
            exchange=exchange,
            current=current,
            lowest=lowest,
            highest=highest,
            currency=currency,
            asset=asset,
            volume=volume
        )

    def is_reaching_support(self, support_resistance: SupportResistanceIndicator, price: Price):
        pass

    def is_reaching_resistance(self, support_resistance: SupportResistanceIndicator, price: Price):
        pass

    def is_through_support(self, support_resistance: SupportResistanceIndicator, price: Price):
        pass

    def is_through_resistance(self, support_resistance: SupportResistanceIndicator, price: Price):
        pass

    def is_over_moving_average(self, moving_average: MovingAverage, compared_by: str = 'close'):
        if compared_by == 'volume':
            return self.volume > moving_average.list_moving_averages[-1]
        elif compared_by == 'close':
            return self.current > moving_average.list_moving_averages[-1]
        elif compared_by == 'lowest':
            return self.lowest > moving_average.list_moving_averages[-1]
        elif compared_by == 'highest':
            return self.highest > moving_average.list_moving_averages[-1]

    def is_under_moving_average(self, moving_average: MovingAverage, compared_by: str = 'close'):
        if compared_by == 'volume':
            return self.volume < moving_average.list_moving_averages[-1]
        elif compared_by == 'close':
            return self.current < moving_average.list_moving_averages[-1]
        elif compared_by == 'lowest':
            return self.lowest < moving_average.list_moving_averages[-1]
        elif compared_by == 'highest':
            return self.highest < moving_average.list_moving_averages[-1]




class SingleStockSampleStrategy(Strategy):
    def __init__(
            self,
            name: str,
            strategy_id: str,
            asset: Asset,
            indicators: list
    ):
        super().__init__(name, strategy_id, asset)
        self.list_indicators = indicators

    def process(self, price: Price):
        """
        Process buy/ sell with single stock
        :param price:
        :return:
        """
        # Rule here
        # If


