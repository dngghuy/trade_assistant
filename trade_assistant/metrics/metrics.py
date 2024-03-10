"""
This file contains the functions for calculating the performance metrics
of a trading strategy.
"""
# Object for calculating Sharpe Ratio
import numpy as np
import pandas as pd


class BaseMetricCalculation:
    def __init__(self, interval: int):
        self.interval = interval

    def calculate(self, *args, **kwargs):
        raise NotImplementedError


class SharpeRatio(BaseMetricCalculation):
    def __init__(self, interval: int = 252, risk_free_rate: float = 0.06):
        super().__init__(interval)
        self.risk_free_rate = risk_free_rate

    def calculate(self, returns: pd.DataFrame):
        return (self.interval ** 0.5)*(returns.mean() - self.risk_free_rate) / returns.std()
