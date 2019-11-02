class StaticStamp:
    def __init__(self, stamp):
        self._stamp = stamp

    def __call__(self):
        return self._stamp


class IncrementingStamp:
    def __init__(self, value: int):
        self._value = value

    def __call__(self):
        return self._value + 1
