import json
import threading
import time
from datetime import datetime
from .price import Price
from .exchange import Exchange
from .order import Order
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

    @abstractmethod
    def run(self):
        pass

    def stop(self):
        self._timer.cancel()
        self._is_running = False

    def get_price(self):
        return self.price

    def set_price(self, price: Price):
        self.price = price

    def buy(self, **kwargs):
        order = Order(
            currency=self.exchange.currency,
            asset=self.exchange.asset,
            symbol=self.exchange.get_symbol(),
            type=Order.TYPE_LIMIT,
            side=Order.BUY,
            test=self.test,
            **kwargs
        )
        self.order(order)

    def sell(self, **kwargs):
        order = Order(
            currency=self.exchange.currency,
            asset=self.exchange.asset,
            symbol=self.exchange.get_symbol(),
            side=Order.SELL,
            test=self.test,
            **kwargs
        )
        self.order(order)

    def order(self, order: Order):
        print(order)
        if self.test:
            exchange_order = self.exchange.test_order(order)
        else:
            exchange_order = self.exchange.order(order)

        print(exchange_order)