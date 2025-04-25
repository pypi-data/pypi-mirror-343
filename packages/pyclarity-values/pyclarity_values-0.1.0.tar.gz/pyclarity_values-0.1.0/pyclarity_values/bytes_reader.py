class BytesReader:
    def __init__(self, arr):
        self.source = arr
        self.consumed = 0

    def read_bytes(self, length):
        view = self.source[self.consumed:self.consumed + length]
        self.consumed += length
        return view

    def read_uint32_be(self):
        return int.from_bytes(self.read_bytes(4), byteorder='big')

    def read_uint8(self):
        return int.from_bytes(self.read_bytes(1), byteorder='big')

    def read_uint16_be(self):
        return int.from_bytes(self.read_bytes(2), byteorder='big')

    def read_big_uint_le(self, length):
        bytes_data = self.read_bytes(length)[::-1]  # Reverse bytes
        hex_data = bytes_data.hex()
        return int(hex_data, 16)

    def read_big_uint_be(self, length):
        bytes_data = self.read_bytes(length)
        hex_data = bytes_data.hex()
        return int(hex_data, 16)

    @property
    def read_offset(self):
        return self.consumed

    @read_offset.setter
    def read_offset(self, val):
        self.consumed = val

    @property
    def internal_bytes(self):
        return self.source

    def read_uint8_enum(self, enum_variable, invalid_enum_error_formatter):
        num = self.read_uint8()
        if num in enum_variable.values():
            return num
        raise invalid_enum_error_formatter(num)


def create_enum_checker(enum_variable):
    enum_values = [v for v in enum_variable.values() if isinstance(v, int)]
    enum_value_set = set(enum_values)

    def checker(value):
        return value in enum_value_set

    return checker


enum_check_functions = {}


def is_enum(enum_variable, value):
    checker = enum_check_functions.get(enum_variable)
    if checker is not None:
        return checker(value)
    new_checker = create_enum_checker(enum_variable)
    enum_check_functions[enum_variable] = new_checker
    return is_enum(enum_variable, value)
