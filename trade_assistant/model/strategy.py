from abc import ABC, abstractmethod
from .asset import Asset

class Strategy(ABC):
    """
    Strategy object
    """
    def __init__(self, name, id, asset: Asset):
        """
        - strategy name
        - strategy id
        Link to asset
        """
        self.name = name
        self.id = id
        self.asset = asset

    def process(self):
        raise NotImplementedError
