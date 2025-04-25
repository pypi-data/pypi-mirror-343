# Define constants
from typing import Union

from .clarity_value import ClarityValue
from .common import serialize_address, serialize_lp_string
from .constants import ClarityType
from .type_boolean_cv import BooleanCV
from .type_buffer_cv import BufferCV
from .type_int_cv import IntCV, UIntCV
from .type_list_cv import ListCV
from .type_optional_cv import OptionalCV, NoneCV
from .type_principal_cv import StandardPrincipalCV, ContractPrincipalCV
from .type_response_cv import ResponseCV
from .type_string_cv import StringAsciiCV, StringUtf8CV
from .type_tuple_cv import TupleCV

CLARITY_INT_BYTE_SIZE = 16
CLARITY_INT_SIZE = 128


class TransactionError(Exception):
    def __init__(self, message):
        super().__init__(message)


class SerializationError(TransactionError):
    def __init__(self, message):
        super().__init__(message)


# Helper functions
def bytes_with_type_id(type_id: ClarityType, byte_array: bytes) -> bytes:
    return bytes([type_id.value]) + byte_array


def serialize_bool_cv(value: BooleanCV) -> bytes:
    return bytes_with_type_id(value.type, bytes([value.type.value]))


def serialize_optional_cv(cv: Union[OptionalCV, NoneCV]) -> bytes:
    if cv.type == ClarityType.OptionalNone:
        return bytes_with_type_id(cv.type, bytes([cv.type.value]))
    else:
        return bytes_with_type_id(cv.type, serialize_cv(cv.value))


def serialize_buffer_cv(cv: BufferCV) -> bytes:
    length_bytes = cv.buffer_length.to_bytes(4, byteorder='big')
    return bytes_with_type_id(cv.type, length_bytes + cv.buffer)


def serialize_int_cv(cv: IntCV) -> bytes:
    byte_array = cv.value.to_bytes(CLARITY_INT_BYTE_SIZE, byteorder='big', signed=True)
    return bytes_with_type_id(cv.type, byte_array)


def serialize_uint_cv(cv: UIntCV) -> bytes:
    byte_array = cv.value.to_bytes(CLARITY_INT_BYTE_SIZE, byteorder='big')
    return bytes_with_type_id(cv.type, byte_array)


def serialize_standard_principal_cv(cv: StandardPrincipalCV) -> bytes:
    return bytes_with_type_id(cv.type, serialize_address(cv.address))


def serialize_contract_principal_cv(cv: ContractPrincipalCV) -> bytes:
    address_bytes = serialize_address(cv.address)
    contract_name_bytes = serialize_lp_string(cv.contract_name)
    return bytes_with_type_id(cv.type, address_bytes + contract_name_bytes)


def serialize_response_cv(cv: ResponseCV) -> bytes:
    return bytes_with_type_id(cv.type, serialize_cv(cv.value))


def serialize_list_cv(cv: ListCV) -> bytes:
    length_bytes = cv.list_length.to_bytes(4, byteorder='big')
    item_bytes = b''.join([serialize_cv(item) for item in cv.list])
    return bytes_with_type_id(cv.type, length_bytes + item_bytes)


def serialize_tuple_cv(cv: TupleCV) -> bytes:
    data_length_bytes = len(cv.data).to_bytes(4, byteorder='big')
    keys = sorted(cv.data.keys())
    key_value_bytes = b''.join([serialize_lp_string(key) + serialize_cv(cv.data[key]) for key in keys])
    return bytes_with_type_id(cv.type, data_length_bytes + key_value_bytes)


def serialize_string_cv(cv: StringAsciiCV, encoding: str) -> bytes:
    str_bytes = cv.data.encode(encoding)
    length_bytes = len(str_bytes).to_bytes(4, byteorder='big')
    return bytes_with_type_id(cv.type, length_bytes + str_bytes)


def serialize_string_ascii_cv(cv: StringAsciiCV) -> bytes:
    return serialize_string_cv(cv, 'ascii')


def serialize_string_utf8_cv(cv: StringUtf8CV) -> bytes:
    return serialize_string_cv(cv, 'utf-8')


# Serialize clarity value to bytes
def serialize_cv(value: ClarityValue) -> bytes:
    if value.type in (ClarityType.BoolTrue, ClarityType.BoolFalse):
        return serialize_bool_cv(value)
    elif value.type in (ClarityType.OptionalNone, ClarityType.OptionalSome):
        return serialize_optional_cv(value)
    elif value.type == ClarityType.Buffer:
        return serialize_buffer_cv(value)
    elif value.type == ClarityType.UInt:
        return serialize_uint_cv(value)
    elif value.type == ClarityType.Int:
        return serialize_int_cv(value)
    elif value.type == ClarityType.PrincipalStandard:
        return serialize_standard_principal_cv(value)
    elif value.type == ClarityType.PrincipalContract:
        return serialize_contract_principal_cv(value)
    elif value.type in (ClarityType.ResponseOk, ClarityType.ResponseErr):
        return serialize_response_cv(value)
    elif value.type == ClarityType.List:
        return serialize_list_cv(value)
    elif value.type == ClarityType.Tuple:
        return serialize_tuple_cv(value)
    elif value.type == ClarityType.StringASCII:
        return serialize_string_ascii_cv(value)
    elif value.type == ClarityType.StringUTF8:
        return serialize_string_utf8_cv(value)
    else:
        raise SerializationError('Unable to serialize. Invalid Clarity Value.')
