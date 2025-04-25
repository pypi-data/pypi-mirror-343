from .constants import ClarityType


# Define a class for BooleanCV
class BooleanCV:
    def __init__(self, clarity_type: ClarityType):
        self.type = clarity_type


class TrueCV(BooleanCV):
    def __init__(self):
        super().__init__(ClarityType.BoolTrue)


class FalseCV(BooleanCV):
    def __init__(self):
        super().__init__(ClarityType.BoolFalse)


def true_cv() -> TrueCV:
    return TrueCV()


def false_cv() -> FalseCV:
    return FalseCV()


def bool_cv(bool_value: bool) -> BooleanCV:
    return true_cv() if bool_value else false_cv()
