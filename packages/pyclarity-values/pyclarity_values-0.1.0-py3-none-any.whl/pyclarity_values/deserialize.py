from typing import Union

from .bytes_reader import BytesReader
from .clarity_value import ClarityValue
from .common import hex_to_bytes, bytes_to_ascii, bytes_to_utf8, create_lp_string
from .constants import ClarityType
from .type_boolean_cv import true_cv, false_cv
from .type_buffer_cv import buffer_cv
from .type_int_cv import int_cv, uint_cv
from .type_list_cv import list_cv
from .type_optional_cv import none_cv, some_cv
from .type_principal_cv import standard_principal_cv_from_address, contract_principal_cv_from_address
from .type_response_cv import response_ok_cv, response_error_cv
from .type_string_cv import string_ascii_cv, string_utf8_cv
from .type_tuple_cv import tuple_cv


class TransactionError(Exception):
    def __init__(self, message):
        super().__init__(message)


class DeserializationError(TransactionError):
    def __init__(self, message):
        super().__init__(message)


import binascii


def deserialize_address(address_bytes):
    version = int(binascii.hexlify(address_bytes[:1]), 16)
    data = binascii.hexlify(address_bytes[1:]).decode('utf-8')

    return {'type': 'StacksMessageType.Address', 'version': version, 'hash160': data}


def deserialize_lp_string(bytes_reader, prefix_bytes=1, max_length=128):
    length_hex = bytes_reader.read_bytes(prefix_bytes).hex()
    length = int(length_hex, 16)
    content = bytes_reader.read_bytes(length).decode('utf-8')
    return create_lp_string(content, prefix_bytes, max_length)


def deserialize_cv(serialized_clarity_value: Union[BytesReader, bytes, str]) -> ClarityValue:
    if isinstance(serialized_clarity_value, str):
        has_hex_prefix = serialized_clarity_value[:2].lower() == '0x'
        bytes_reader = BytesReader(
            hex_to_bytes(serialized_clarity_value[2:]) if has_hex_prefix else hex_to_bytes(serialized_clarity_value)
        )
    elif isinstance(serialized_clarity_value, bytes):
        bytes_reader = BytesReader(serialized_clarity_value)
    else:
        bytes_reader = serialized_clarity_value

    type = bytes_reader.read_uint8_enum(ClarityType,
                                        lambda n: DeserializationError(f'Cannot recognize Clarity Type: {n}'))

    if type == ClarityType.Int.value:
        return int_cv(bytes_reader.read_bytes(16))
    elif type == ClarityType.UInt.value:
        return uint_cv(bytes_reader.read_bytes(16))
    elif type == ClarityType.Buffer.value:
        buffer_length = bytes_reader.read_uint32_be()
        return buffer_cv(bytes_reader.read_bytes(buffer_length))
    elif type == ClarityType.BoolTrue.value:
        return true_cv()
    elif type == ClarityType.BoolFalse.value:
        return false_cv()
    elif type == ClarityType.PrincipalStandard.value:
        s_address = deserialize_address(bytes_reader.internal_bytes)
        return standard_principal_cv_from_address(s_address)
    elif type == ClarityType.PrincipalContract.value:
        c_address = deserialize_address(bytes_reader.internal_bytes)
        contract_name = deserialize_lp_string(bytes_reader.internal_bytes)
        return contract_principal_cv_from_address(c_address, contract_name)
    elif type == ClarityType.ResponseOk.value:
        return response_ok_cv(deserialize_cv(bytes_reader))
    elif type == ClarityType.ResponseErr.value:
        return response_error_cv(deserialize_cv(bytes_reader))
    elif type == ClarityType.OptionalNone.value:
        return none_cv()
    elif type == ClarityType.OptionalSome.value:
        return some_cv(deserialize_cv(bytes_reader))
    elif type == ClarityType.List.value:
        list_length = bytes_reader.read_uint32_be()
        list_contents = []
        for _ in range(list_length):
            list_contents.append(deserialize_cv(bytes_reader))
        return list_cv(list_contents)
    elif type == ClarityType.Tuple.value:
        tuple_length = bytes_reader.read_uint32_be()
        tuple_contents = {}
        for _ in range(tuple_length):
            clarity_name = deserialize_lp_string(bytes_reader).content
            tuple_contents[clarity_name] = deserialize_cv(bytes_reader)
        return tuple_cv(tuple_contents)
    elif type == ClarityType.StringASCII.value:
        ascii_str_len = bytes_reader.read_uint32_be()
        ascii_str = bytes_to_ascii(bytes_reader.read_bytes(ascii_str_len))
        return string_ascii_cv(ascii_str)
    elif type == ClarityType.StringUTF8.value:
        utf8_str_len = bytes_reader.read_uint32_be()
        utf8_str = bytes_to_utf8(bytes_reader.read_bytes(utf8_str_len))
        return string_utf8_cv(utf8_str)
    else:
        raise DeserializationError('Unable to deserialize Clarity Value from bytes. Could not find valid Clarity Type.')
