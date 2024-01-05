"""

"""
import numpy as np
import pandas as pd
from trade_assistant.signal_processing.base import Indicator


class MovingAverage(Indicator):
    rolling_wave_length: int = None
    col: str = None

    def __init__(self, rolling_wave_length: int, col: str = 'close'):
        super().__init__(rolling_wave_length=rolling_wave_length, col=col)
        self.list_moving_averages = []

    def process(self, input_df: pd.DataFrame):
        moving_averages = input_df[self.col].rolling(self.rolling_wave_length).mean()
        self.list_moving_averages.append(moving_averages)
