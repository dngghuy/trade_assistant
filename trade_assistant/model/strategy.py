from abc import ABC, abstractmethod
from .asset import Asset


class Strategy(ABC):
    """
    Strategy object
    """
    def __init__(self, name: str, strategy_id: str, asset: Asset):
        """
        - strategy name
        - strategy id
        Link to asset
        """
        self.name = name
        self.strategy_id = strategy_id
        self.asset = asset

    def process(self, *args, **kwargs):
        raise NotImplementedError
