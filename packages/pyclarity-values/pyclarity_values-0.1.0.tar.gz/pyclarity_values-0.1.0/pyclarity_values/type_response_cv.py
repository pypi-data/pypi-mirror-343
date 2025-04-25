from dataclasses import dataclass

from .clarity_value import ClarityValue
from .constants import ClarityType


@dataclass
class ResponseCV:
    type: ClarityType.ResponseErr or ClarityType.ResponseOk
    value: ClarityValue

@dataclass
class ResponseErrorCV:
    type: ClarityType.ResponseErr
    value: ClarityValue

@dataclass
class ResponseOkCV:
    type: ClarityType.ResponseOk
    value: ClarityValue

def response_error_cv(value: ClarityValue) -> ResponseErrorCV:
    return ResponseErrorCV(type=ClarityType.ResponseErr, value=value)

def response_ok_cv(value: ClarityValue) -> ResponseOkCV:
    return ResponseOkCV(type=ClarityType.ResponseOk, value=value)
