from enum import Enum


# Define ClarityType enum
class ClarityType(Enum):
    Int = 0x00
    UInt = 0x01
    Buffer = 0x02
    BoolTrue = 0x03
    BoolFalse = 0x04
    PrincipalStandard = 0x05
    PrincipalContract = 0x06
    ResponseOk = 0x07
    ResponseErr = 0x08
    OptionalNone = 0x09
    OptionalSome = 0x0a
    List = 0x0b
    Tuple = 0x0c
    StringASCII = 0x0d
    StringUTF8 = 0x0e

    @classmethod
    def values(cls):
        return list(map(lambda c: c.value, cls))


class StacksMessageType(Enum):
    Address = 1
    Principal = 2
    LengthPrefixedString = 3
    MemoString = 4
    AssetInfo = 5
    PostCondition = 6
    PublicKey = 7
    LengthPrefixedList = 8
    Payload = 9
    MessageSignature = 10
    StructuredDataSignature = 11
    TransactionAuthField = 12
