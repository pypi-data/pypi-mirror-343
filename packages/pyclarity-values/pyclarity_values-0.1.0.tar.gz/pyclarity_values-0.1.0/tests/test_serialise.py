from pyclarity_values import *

def test_serialize_uint():
    cv = UIntCV(42)
    serialized = serialize_cv(cv)
    assert serialized.hex() == "010000000000000000000000000000002a"


def test_serialize_int():
    cv = IntCV(42)
    serialized = serialize_cv(cv)
    assert serialized.hex() == "000000000000000000000000000000002a"


def test_serialize_true_false():
    assert serialize_cv(true_cv()).hex() == "0303"
    assert serialize_cv(false_cv()).hex() == "0404"


def test_serialize_buffer():
    cv = buffer_cv(b"abc")
    serialized = serialize_cv(cv)
    assert serialized.hex() == "0200000003616263"


def test_serialize_string_ascii():
    cv = string_ascii_cv("clarity")
    serialized = serialize_cv(cv)
    assert serialized.hex() == "0d00000007636c6172697479"


def test_serialize_string_utf8():
    cv = string_utf8_cv("Cogito, ergo sum")
    serialized = serialize_cv(cv)
    assert serialized.hex() == "0e00000010436f6769746f2c206572676f2073756d"


def test_serialize_optional_none():
    serialized = serialize_cv(none_cv())
    assert serialized.hex() == "0909"


def test_serialize_optional_some():
    cv = some_cv(UIntCV(42))
    serialized = serialize_cv(cv)
    assert serialized.hex() == "0a010000000000000000000000000000002a"


def test_serialize_response_ok():
    cv = response_ok_cv(UIntCV(42))
    serialized = serialize_cv(cv)
    assert serialized.hex() == "07010000000000000000000000000000002a"


def test_serialize_response_err():
    cv = response_error_cv(UIntCV(42))
    serialized = serialize_cv(cv)
    assert serialized.hex() == "08010000000000000000000000000000002a"