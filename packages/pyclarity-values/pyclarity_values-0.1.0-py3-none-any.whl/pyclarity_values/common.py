import re

from dataclasses import dataclass
from typing import Union, List

from .constants import StacksMessageType

from enum import Enum


class PostConditionPrincipalID(Enum):
    Origin = 0x01
    Standard = 0x02
    Contract = 0x03


class AddressVersion(Enum):
    MainnetSingleSig = 22
    MainnetMultiSig = 20
    TestnetSingleSig = 26
    TestnetMultiSig = 21


def next_year():
    from datetime import datetime, timedelta
    return datetime.now() + timedelta(days=365)


def next_month():
    from datetime import datetime, timedelta
    return datetime.now() + timedelta(days=30)


def next_hour():
    from datetime import datetime, timedelta
    return datetime.now() + timedelta(hours=1)


def megabytes_to_bytes(megabytes: float) -> int:
    if not isinstance(megabytes, (int, float)) or not is_finite(megabytes):
        return 0
    return int(megabytes * 1024 * 1024)


def get_aes_cbc_output_length(input_byte_length: int) -> int:
    return (input_byte_length // 16 + 1) * 16


def get_base64_output_length(input_byte_length: int) -> int:
    return (input_byte_length // 3 + 1) * 4


def update_query_string_parameter(uri: str, key: str, value: str) -> str:
    from urllib.parse import urlparse, urlencode, parse_qs, urlunparse
    scheme, netloc, path, params, query, fragment = urlparse(uri)
    query_dict = parse_qs(query)
    query_dict[key] = [value]
    updated_query = urlencode(query_dict, doseq=True)
    return urlunparse((scheme, netloc, path, params, updated_query, fragment))


def is_later_version(v1: str, v2: str) -> bool:
    v1 = v1 if v1 else '0.0.0'
    v2 = v2 if v2 else '0.0.0'
    v1_tuple = [int(x) for x in v1.split('.')]
    v2_tuple = [int(x) for x in v2.split('.')]
    for i in range(len(v2_tuple)):
        if i >= len(v1_tuple):
            v1_tuple.append(0)
        if v1_tuple[i] < v2_tuple[i]:
            return False
    return True


def make_uuid4():
    from uuid import uuid4
    return str(uuid4())


def is_same_origin_absolute_url(uri1: str, uri2: str) -> bool:
    try:
        from urllib.parse import urlparse
        parsed_uri1 = urlparse(uri1)
        parsed_uri2 = urlparse(uri2)
        port1 = int(parsed_uri1.port) if parsed_uri1.port else (443 if parsed_uri1.scheme == 'https' else 80)
        port2 = int(parsed_uri2.port) if parsed_uri2.port else (443 if parsed_uri2.scheme == 'https' else 80)
        match = {
            'scheme': parsed_uri1.scheme == parsed_uri2.scheme,
            'hostname': parsed_uri1.hostname == parsed_uri2.hostname,
            'port': port1 == port2,
            'absolute': (uri1.startswith('http://') or uri1.startswith('https://')) and (
                    uri2.startswith('http://') or uri2.startswith('https://'))
        }
        return all(match.values())
    except Exception as e:
        print(e)
        print('Parsing error in same URL origin check')
        return False


def get_global_scope():
    try:
        from browser import window
        return window
    except ImportError:
        pass

    try:
        from node import global_
        return global_
    except ImportError:
        pass

    raise RuntimeError(
        'Unexpected runtime environment - no supported global scope (`window`, `self`, `global`) available')


def get_global_object(name: str, throw_if_unavailable=False, usage_desc=None, return_empty_object=False):
    global_scope = get_global_scope()
    obj = getattr(global_scope, name, None)
    if obj is not None:
        return obj
    if throw_if_unavailable:
        raise RuntimeError(
            f"`{name}` is unavailable on the '{global_scope}' object within the currently executing environment.")
    if return_empty_object:
        return {}
    return None


def get_global_objects(names: List[str], throw_if_unavailable=False, usage_desc=None, return_empty_object=False):
    result = {}
    global_scope = get_global_scope()
    for name in names:
        obj = getattr(global_scope, name, None)
        if obj is not None:
            result[name] = obj
        elif throw_if_unavailable:
            raise RuntimeError(
                f"`{name}` is unavailable on the '{global_scope}' object within the currently executing environment.")
        elif return_empty_object:
            result[name] = {}
    return result


def int_to_bytes(value: Union[int, str, int], signed: bool, byte_length: int) -> bytes:
    big_int = int_to_bigint(value, signed)
    return big_int_to_bytes(big_int, byte_length)


def int_to_bigint(value: Union[int, str, bytes], signed: bool) -> int:
    try:
        parsed_value = int(value)
        if isinstance(parsed_value, int):
            if not is_integer(parsed_value):
                raise ValueError("Invalid value. Values of type 'int' must be an integer.")
            return parsed_value
    except ValueError:
        pass

    if isinstance(value, str):
        if value.lower().startswith("0x"):
            # Trim '0x' hex-prefix
            hex_value = value[2:]
            # Allow odd-length strings like `0xf` -- some libs output these, or even just `0x${num.toString(16)}`
            hex_value = hex_value.zfill((len(hex_value) + (len(hex_value) % 2)))
            parsed_value = bytes.fromhex(hex_value)
        else:
            try:
                return int(value)
            except ValueError:
                raise ValueError(f"Invalid value. String integer '{value}' is not a valid integer.")

    if isinstance(value, bytes):
        if signed:
            byte_length_bits = len(value) * 8
            bn = int.from_bytes(value, byteorder='big', signed=True)
            if bn >= (2 ** (byte_length_bits - 1)):
                bn = bn - (2 ** byte_length_bits)
            return bn
        else:
            return int.from_bytes(value, byteorder='big')

    raise TypeError("Invalid value type. Must be an int, integer-string, hex-string, or bytes.")


def is_integer(value):
    return isinstance(value, int)


def hex_to_bytes(hex_string):
    if len(hex_string) % 2 != 0:
        hex_string = '0' + hex_string  # Pad with '0' if the string has an odd length
    return bytes.fromhex(hex_string)


def bytes_to_hex(byte_array):
    return byte_array.hex()


def from_twos(value, width):
    if value < -(1 << (width - 1)) or (1 << (width - 1)) - 1 < value:
        raise ValueError(f"Unable to represent integer in width: {width}")
    if value >= 0:
        return value
    return value + (1 << width)


def with_0x(value: str) -> str:
    return value if value.startswith('0x') else f'0x{value}'


def hex_to_bigint(hex_string: str) -> int:
    if not isinstance(hex_string, str):
        raise TypeError(f"hex_to_bigint: expected string, got {type(hex_string)}")
    return int(hex_string, 16)


def int_to_hex(integer: Union[int, str, int], length_bytes: int = 8) -> str:
    value = integer if isinstance(integer, int) else int_to_bigint(integer, False)
    return hex(value)[2:].zfill(length_bytes * 2)


def hex_to_int(hex_string: str) -> int:
    return int(hex_string, 16)


def big_int_to_bytes(value: int, length: int = 16) -> bytes:
    hex_str = hex(value)[2:]
    if len(hex_str) % 2 != 0:
        hex_str = '0' + hex_str
    return bytes.fromhex(hex_str.zfill(length * 2))


def to_twos(value: int, width: int) -> int:
    min_value = -(1 << (width - 1))
    max_value = (1 << (width - 1)) - 1
    if value < min_value or value > max_value:
        raise ValueError(f"Unable to represent integer in width: {width}")
    if value >= 0:
        return value
    return value + (1 << width)


def from_twos(value: int, width: int) -> int:
    if value & (1 << (width - 1)):
        return value - (1 << width)
    return value


def bytes_to_hex(uint8a: bytes) -> str:
    return uint8a.hex()


def hex_to_bytes(hex_string: str) -> bytes:
    return bytes.fromhex(hex_string)


def utf8_to_bytes(utf8_string: str) -> bytes:
    return utf8_string.encode('utf-8')


def bytes_to_utf8(arr: bytes) -> str:
    return arr.decode('utf-8')


def ascii_to_bytes(ascii_string: str) -> bytes:
    return bytes(ascii_string, 'ascii')


def bytes_to_ascii(arr: bytes) -> str:
    return arr.decode('ascii')


def octets_to_bytes(numbers: List[int]) -> bytes:
    if any(not isinstance(n, int) or n < 0 or n > 255 for n in numbers):
        raise ValueError('Some values are invalid bytes.')
    return bytes(numbers)


def to_bytes(data: Union[bytes, str]) -> bytes:
    if isinstance(data, str):
        return utf8_to_bytes(data)
    if isinstance(data, bytes):
        return data
    raise TypeError(f"Expected input type is (bytes or str), but got {type(data)}")


def concat_bytes(*arrays: bytes) -> bytes:
    return b''.join(arrays)


def concat_array(elements: List[Union[bytes, List[int], int]]) -> bytes:
    byte_elements = []
    for element in elements:
        if isinstance(element, int):
            byte_elements.append(octets_to_bytes([element]))
        elif isinstance(element, list):
            byte_elements.append(octets_to_bytes(element))
        elif isinstance(element, bytes):
            byte_elements.append(element)
        else:
            raise TypeError(f"Invalid element type: {type(element)}")
    return concat_bytes(*byte_elements)


def is_instance(object, type_):
    return isinstance(object, type_) or (hasattr(object, '__class__') and object.__class__.__name__ == type_.__name__)


def is_finite(value: float) -> bool:
    return not (value == float('inf') or value == float('-inf') or value != value)


def address_to_string(address: any) -> str:
    return c32address(address.version, address.hash160)


def c32address(version, hash160hex):
    if not all(c in '0123456789abcdefABCDEF' for c in hash160hex) or len(hash160hex) != 40:
        raise ValueError('Invalid argument: not a hash160 hex string')
    c32string = c32check_encode(version, hash160hex)
    return 'S' + c32string


def c32address_decode(c32addr):
    if len(c32addr) <= 5:
        raise ValueError('Invalid c32 address: invalid length')
    if c32addr[0] != 'S':
        raise ValueError('Invalid c32 address: must start with "S"')
    return c32check_decode(c32addr[1:])


import hashlib

c32 = '0123456789ABCDEFGHJKMNPQRSTVWXYZ'
hex_chars = '0123456789abcdef'


def c32checksum(data_hex):
    data_hash = hashlib.sha256(hashlib.sha256(bytes.fromhex(data_hex)).digest()).digest()
    checksum = data_hash[:4]
    return checksum.hex()


def c32check_encode(version, data):
    if version < 0 or version >= 32:
        raise ValueError('Invalid version (must be between 0 and 31)')
    if not all(c in '0123456789abcdefABCDEF' for c in data):
        raise ValueError('Invalid data (not a hex string)')
    data = data.lower()
    if len(data) % 2 != 0:
        data = '0' + data
    version_hex = format(version, '02x')
    if len(version_hex) == 1:
        version_hex = '0' + version_hex
    checksum_hex = c32checksum(version_hex + data)
    c32_str = c32encode(data + checksum_hex)
    return c32[version] + c32_str


def c32encode(input_hex, min_length=None):
    if not all(c in '0123456789abcdefABCDEF' for c in input_hex):
        raise ValueError('Not a hex-encoded string')
    if len(input_hex) % 2 != 0:
        input_hex = '0' + input_hex
    input_hex = input_hex.lower()
    res = []
    carry = 0
    for i in range(len(input_hex) - 1, -1, -1):
        if carry < 4:
            current_code = hex_chars.index(input_hex[i]) >> carry
            next_code = 0
            if i != 0:
                next_code = hex_chars.index(input_hex[i - 1])
            next_bits = 1 + carry
            next_low_bits = next_code % (1 << next_bits) << (5 - next_bits)
            cur_c32_digit = c32[current_code + next_low_bits]
            carry = next_bits
            res.insert(0, cur_c32_digit)
        else:
            carry = 0
    C32leadingZeros = 0
    for i in range(len(res)):
        if res[i] != '0':
            break
        else:
            C32leadingZeros += 1
    res = res[C32leadingZeros:]
    zero_prefix = bytes.fromhex(input_hex).lstrip(b'\x00')
    num_leading_zero_bytes_in_hex = len(bytes.fromhex(input_hex)) - len(zero_prefix)
    for i in range(num_leading_zero_bytes_in_hex):
        res.insert(0, c32[0])
    if min_length:
        count = min_length - len(res)
        for i in range(count):
            res.insert(0, c32[0])
    return ''.join(res)


def c32check_decode(c32data):
    c32data = c32normalize(c32data)
    data_hex = c32decode(c32data[1:])
    version_char = c32data[0]
    version = c32.index(version_char)
    checksum = data_hex[-8:]

    version_hex = hex(version)[2:]
    if len(version_hex) == 1:
        version_hex = '0' + version_hex

    if c32checksum(f'{version_hex}{data_hex[:-8]}') != checksum:
        raise ValueError('Invalid c32check string: checksum mismatch')

    return [version, data_hex[:-8]]


def c32normalize(c32input):
    # must be upper-case
    # replace all O's with 0's
    # replace all I's and L's with 1's
    return c32input.upper().replace('O', '0').replace('I', '1').replace('L', '1')


def c32decode(c32input, minLength=None):
    c32input = c32normalize(c32input)

    # must result in a c32 string
    if not all(c in c32 for c in c32input):
        raise ValueError('Not a c32-encoded string')

    zero_prefix = re.match(f'^[{c32[0]}]*', c32input)
    num_leading_zero_bytes = len(zero_prefix.group(0)) if zero_prefix else 0

    res = []
    carry = 0
    carry_bits = 0
    for i in range(len(c32input) - 1, -1, -1):
        if carry_bits == 4:
            res.insert(0, hex(carry)[2:])
            carry_bits = 0
            carry = 0
        current_code = c32.index(c32input[i]) << carry_bits
        current_value = current_code + carry
        current_hex_digit = hex(current_value % 16)[2:]
        carry_bits += 1
        carry = current_value >> 4
        if carry > 1 << carry_bits:
            raise ValueError('Panic error in decoding.')
        res.insert(0, current_hex_digit)
    # one last carry
    res.insert(0, hex(carry)[2:])

    if len(res) % 2 == 1:
        res.insert(0, '0')

    hex_leading_zeros = 0
    for i in range(len(res)):
        if res[i] != '0':
            break
        else:
            hex_leading_zeros += 1

    res = res[hex_leading_zeros - (hex_leading_zeros % 2):]

    hex_str = ''.join(res)
    for i in range(num_leading_zero_bytes):
        hex_str = f'00{hex_str}'

    if minLength:
        count = minLength * 2 - len(hex_str)
        for i in range(0, count, 2):
            hex_str = f'00{hex_str}'

    return hex_str


@dataclass
class LengthPrefixedString:
    type: StacksMessageType.LengthPrefixedString
    content: str
    lengthPrefixBytes: int
    maxLengthBytes: int

    @property
    def length(self) -> int:
        return len(self.content.encode('utf-8'))

    @property
    def bytes(self) -> bytes:
        length_bytes = self.length.to_bytes(self.lengthPrefixBytes, 'big')
        content_bytes = self.content.encode('utf-8')
        return length_bytes + content_bytes

    @property
    def hex(self) -> str:
        return self.bytes.hex()

    @property
    def value(self) -> str:
        return self.content

    def encode(self, encoding: str) -> bytes:
        return self.content.encode(encoding)


MAX_STRING_LENGTH_BYTES = 128


def create_lp_string(content: str, lengthPrefixBytes: int = 1, maxLengthBytes: int = MAX_STRING_LENGTH_BYTES):
    prefixLength = lengthPrefixBytes
    max_length = maxLengthBytes
    if exceeds_max_length_bytes(content, max_length):
        raise Exception(f"String length exceeds maximum bytes {max_length}")
    return LengthPrefixedString(type=StacksMessageType.LengthPrefixedString, content=content,
                                lengthPrefixBytes=prefixLength, maxLengthBytes=max_length)


def exceeds_max_length_bytes(string: str, max_length_bytes: int) -> bool:
    return len(string.encode('utf-8')) > max_length_bytes


def is_clarity_name(name: str) -> bool:
    regex = re.compile(r"^[a-zA-Z]([a-zA-Z0-9]|[-_!?+<>=/*])*$|^[-+=/*]$|^[<>]=?$")
    return bool(regex.match(name)) and len(name) < 128


def serialize_address(address):
    bytes_array = []
    bytes_array.append(int.to_bytes(address.version, 1, byteorder='big'))
    bytes_array.append(bytes.fromhex(address.hash160))
    return b''.join(bytes_array)


def serialize_lp_string(lps):
    bytes_array = []
    if isinstance(lps, str):
        lps = create_lp_string(lps)
    content_bytes = lps.content.encode('utf-8')
    length = len(content_bytes)
    bytes_array.append(length.to_bytes(lps.lengthPrefixBytes, 'big'))
    bytes_array.append(content_bytes)
    return b''.join(bytes_array)


def serialize_principal(principal):
    bytes_array = []
    bytes_array.append(principal.prefix)
    bytes_array.append(serialize_address(principal.address))
    if principal.prefix == PostConditionPrincipalID.Contract:
        bytes_array.append(serialize_lp_string(principal.contractName))
    return b''.join(bytes_array)
