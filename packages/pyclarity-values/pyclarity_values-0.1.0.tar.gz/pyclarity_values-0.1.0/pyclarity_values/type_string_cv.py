from dataclasses import dataclass

from .constants import ClarityType

class StringCV:
    @property
    def value(self):
        return self.data

@dataclass
class StringAsciiCV(StringCV):
    type: ClarityType.StringASCII
    data: str

@dataclass
class StringUtf8CV(StringCV):
    type: ClarityType.StringUTF8
    data: str

def string_ascii_cv(data: str) -> StringAsciiCV:
    return StringAsciiCV(type=ClarityType.StringASCII, data=data)

def string_utf8_cv(data: str) -> StringUtf8CV:
    return StringUtf8CV(type=ClarityType.StringUTF8, data=data)

def string_cv(data: str, encoding: str = 'utf8') -> StringAsciiCV or StringUtf8CV:
    if encoding == 'ascii':
        return string_ascii_cv(data)
    elif encoding == 'utf8':
        return string_utf8_cv(data)
