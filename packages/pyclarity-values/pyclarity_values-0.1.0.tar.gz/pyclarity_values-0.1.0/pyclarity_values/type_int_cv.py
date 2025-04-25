from .common import int_to_bigint
from .constants import ClarityType

MAX_U128 = 0xffffffffffffffffffffffffffffffff  # (2 ** 128 - 1)
MIN_U128 = 0
MAX_I128 = 0x7fffffffffffffffffffffffffffffff  # (2 ** 127 - 1)
MIN_I128 = -170141183460469231731687303715884105728  # (-2 ** 127)


class IntCV:
    def __init__(self, value):
        big_int = int_to_bigint(value, signed=True)
        if big_int > MAX_I128:
            raise ValueError(f"Cannot construct clarity integer from value greater than {MAX_I128}")
        elif big_int < MIN_I128:
            raise ValueError(f"Cannot construct clarity integer from value less than {MIN_I128}")
        self.type = ClarityType.Int
        self.value = big_int


class UIntCV:
    def __init__(self, value):
        big_int = int_to_bigint(value, signed=False)
        if big_int < MIN_U128:
            raise ValueError("Cannot construct unsigned clarity integer from negative value")
        elif big_int > MAX_U128:
            raise ValueError(f"Cannot construct unsigned clarity integer greater than {MAX_U128}")
        self.type = ClarityType.UInt
        self.value = big_int


def int_cv(value):
    return IntCV(value)


def uint_cv(value):
    return UIntCV(value)
