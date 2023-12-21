class Indicator:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def process(self, *args, **kwargs):
        raise NotImplementedError

