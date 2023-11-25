import json
import threading
import time
from datetime import datetime
from .price import Price
from .exchange import Exchange
from abc import ABC, abstractmethod


class Strategy:
    TEST_MODE = 'test'
    PROD_MODE = 'prod'
    price: Price

    def __init__(
        self,
        exchange: Exchange,
        interval: int = 60,
        *args,
        **kwargs
    ):
        self._timer = None
        self.interval = interval
        self.args = args
        self.kwargs = kwargs
        self._is_running = False
        self._next_call = time.time()
        self.portfolio = {}
        self.exchange = exchange
        # Load portfolio
        self._get_portfolio()

    def _get_portfolio(self):
        self.portfolio = {
            'currency': self.exchange.get_asset_balance(self.exchange.currency),
            'asset': self.exchange.get_asset_balance(self.exchange.asset)
        }

    def _run(self):
        self._is_running = False
        self.start()
        self.run(*self.args, **self.kwargs)

    def start(self):
        if not self._is_running:
            if self._timer is None:
                self._next_call = time.time()
            else:
                self._next_call += self.interval

            self._timer = threading.Timer(
                self._next_call - time.time(),
                self._run
            )
            self._timer.start()
            self._is_running = True
