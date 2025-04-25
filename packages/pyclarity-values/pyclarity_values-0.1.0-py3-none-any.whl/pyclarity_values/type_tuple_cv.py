from dataclasses import dataclass

from .common import is_clarity_name
from .constants import ClarityType


@dataclass
class TupleCV:
    type: ClarityType.Tuple
    data: dict

    @property
    def value(self):
        return self.data

def tuple_cv(data: dict) -> TupleCV:
    for key in data.keys():
        if not is_clarity_name(key):
            raise ValueError(f'"{key}" is not a valid Clarity name')
    return TupleCV(type=ClarityType.Tuple, data=data)
