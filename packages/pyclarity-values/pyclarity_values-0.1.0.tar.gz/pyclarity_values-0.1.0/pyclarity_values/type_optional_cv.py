from .constants import ClarityType


class OptionalCV:
    def __init__(self, value=None):
        self.value = value
        if value is None:
            self.type = ClarityType.OptionalNone
        else:
            self.type = ClarityType.OptionalSome


class NoneCV:
    def __init__(self):
        self.type = ClarityType.OptionalNone

    @property
    def value(self):
        return None


class SomeCV:
    def __init__(self, value):
        self.type = ClarityType.OptionalSome
        self.value = value


def none_cv():
    return NoneCV()


def some_cv(value):
    return SomeCV(value)


def optional_cv_of(value=None):
    if value is not None:
        return some_cv(value)
    else:
        return none_cv()
