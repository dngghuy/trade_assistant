from .abstract import AbstractModel


class Price(AbstractModel):
    pair: str = ''
    exchange: str = ''
    current: float = 0
    lowest: float = 0
    highest: float = 0
    currency: str = ''
    asset: str = ''
    volume: float = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pair = self._get_pair()

    def _get_pair(self):
        return f'{self.currency}_{self.asset}'
