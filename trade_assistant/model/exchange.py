from .abstract import AbstractModel


class Exchange(AbstractModel):
    resource_name = 'exchanges'

    id: str = ''
    name: str = ''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
