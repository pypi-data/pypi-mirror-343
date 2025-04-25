from typing import Any, Dict
from .constants import ClarityType
from .type_principal_cv import principal_to_string


class ClarityValue:
    def __init__(self, type: ClarityType, value: Any):
        self.type = type
        self.value = value


def cv_to_string(val: ClarityValue, encoding: str = 'hex') -> str:
    if val.type == ClarityType.BoolTrue:
        return 'true'
    elif val.type == ClarityType.BoolFalse:
        return 'false'
    elif val.type == ClarityType.Int:
        return str(val.value)
    elif val.type == ClarityType.UInt:
        return f'u{val.value}'
    elif val.type == ClarityType.Buffer:
        if encoding == 'tryAscii':
            str_val = val.value.decode('utf-8', 'ignore')
            if all(ord(c) < 128 and c.isprintable() for c in str_val):
                return f'"{str_val}"'
        return f'0x{val.value.hex()}'
    elif val.type == ClarityType.OptionalNone:
        return 'none'
    elif val.type == ClarityType.OptionalSome:
        return f'(some {cv_to_string(val.value, encoding)})'
    elif val.type == ClarityType.ResponseErr:
        return f'(err {cv_to_string(val.value, encoding)})'
    elif val.type == ClarityType.ResponseOk:
        return f'(ok {cv_to_string(val.value, encoding)})'
    elif val.type in (ClarityType.PrincipalStandard, ClarityType.PrincipalContract):
        return principal_to_string(val)
    elif val.type == ClarityType.List:
        return f'(list {" ".join(cv_to_string(item, encoding) for item in val.value)})'
    elif val.type == ClarityType.Tuple:
        return f'(tuple {" ".join(f"({key} {cv_to_string(item, encoding)})" for key, item in val.value.items())})'
    elif val.type == ClarityType.StringASCII:
        return f'"{val.value}"'
    elif val.type == ClarityType.StringUTF8:
        return f'u"{val.value}"'


def cv_to_value(val: ClarityValue, strict_json_compat: bool = False) -> Any:
    if val.type in (ClarityType.BoolTrue, ClarityType.BoolFalse, ClarityType.Int, ClarityType.UInt):
        return val.value if strict_json_compat else str(val.value)
    elif val.type == ClarityType.Buffer:
        return f'0x{val.value.hex()}'
    elif val.type == ClarityType.OptionalNone:
        return None
    elif val.type == ClarityType.OptionalSome:
        return cv_to_json(val.value)
    elif val.type in (ClarityType.ResponseErr, ClarityType.ResponseOk):
        return cv_to_json(val.value)
    elif val.type in (ClarityType.PrincipalStandard, ClarityType.PrincipalContract):
        return principal_to_string(val)
    elif val.type == ClarityType.List:
        return [cv_to_json(item) for item in val.value]
    elif val.type == ClarityType.Tuple:
        return {key: cv_to_json(item) for key, item in val.value.items()}
    elif val.type in (ClarityType.StringASCII, ClarityType.StringUTF8):
        return val.value


def cv_to_json(val: ClarityValue) -> Dict[str, Any]:
    result = {'type': get_cv_type_string(val), 'value': cv_to_value(val, True)}
    if val.type == ClarityType.ResponseErr:
        result['success'] = False
    elif val.type == ClarityType.ResponseOk:
        result['success'] = True
    return result


def get_cv_type_string(val: ClarityValue) -> str:
    if val.type == ClarityType.BoolTrue:
        return 'bool'
    elif val.type == ClarityType.BoolFalse:
        return 'bool'
    elif val.type == ClarityType.Int:
        return 'int'
    elif val.type == ClarityType.UInt:
        return 'uint'
    elif val.type == ClarityType.Buffer:
        return f'(buff {len(val.value)})'
    elif val.type == ClarityType.OptionalNone:
        return '(optional none)'
    elif val.type == ClarityType.OptionalSome:
        return f'(optional {get_cv_type_string(val.value)})'
    elif val.type == ClarityType.ResponseErr:
        return f'(response UnknownType {get_cv_type_string(val.value)})'
    elif val.type == ClarityType.ResponseOk:
        return f'(response {get_cv_type_string(val.value)} UnknownType)'
    elif val.type in (ClarityType.PrincipalStandard, ClarityType.PrincipalContract):
        return 'principal'
    elif val.type == ClarityType.List:
        return f'(list {len(val.value)} {get_cv_type_string(val.value[0]) if val.value else "UnknownType"})'
    elif val.type == ClarityType.Tuple:
        return f'(tuple {" ".join(f"({key} {get_cv_type_string(item)})" for key, item in val.value.items())})'
    elif val.type == ClarityType.StringASCII:
        return f'(string-ascii {len(val.value)})'
    elif val.type == ClarityType.StringUTF8:
        return f'(string-utf8 {len(val.value)})'

