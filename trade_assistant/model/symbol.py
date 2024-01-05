from .abstract import AbstractModel


class Symbol(AbstractModel):
    symbol: str = ''
    exchange: str = ''
    current: float = 0
    lowest: float = 0
    highest: float = 0
    currency: str = ''
    volume: float = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


