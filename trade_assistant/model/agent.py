from trade_assistant.consts import DATA_FOLDER
from .strategy import Strategy
from .order import Order
from .consts import OrderType
import pandas as pd
import os


class Agent:
    def __init__(self, exchange, name, asset, strategy: Strategy):
        # Which type of trade - Binance, Stock
        # What are the strategy - Strategy class
        # name
        self.name = name
        self.exchange = exchange
        self.asset = asset
        self.strategy = strategy
        # currently, update to a csv file
        self.log_file_path = DATA_FOLDER / f'{name}_{exchange}_{strategy.name}.csv'
        # If file, open pandas df:
        if os.path.exists(self.log_file_path):
            self.log_df = pd.read_csv(self.log_file_path)
        else:
            self.log_df = pd.DataFrame()
        # open log file

    def run(self, data_feed):
        order = self.strategy.process()

        # handle amount here - update asset
        if order.type == OrderType.HOLD:
            return
        else:
            self.asset.update(order)
            # update
            # log the action, amount, asset balance in to a pandas Series then append to DF
            self.log_df.append([])
            return

    def save_log(self):
        self.log_df.to_csv(self.log_file_path)

