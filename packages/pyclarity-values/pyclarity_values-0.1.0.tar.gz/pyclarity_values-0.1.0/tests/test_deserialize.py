from pyclarity_values import *


def test_deserialize_uint():
    hex_input = "0100000000000000000000000000002a"  # UInt(42)
    cv = deserialize_cv(bytes.fromhex(hex_input))
    assert cv.type == ClarityType.UInt
    assert cv.value == 42


def test_deserialize_int():
    hex_input = "0000000000000000000000000000002a"  # Int(42)
    cv = deserialize_cv(bytes.fromhex(hex_input))
    assert cv.type == ClarityType.Int
    assert cv.value == 42


def test_deserialize_principal():
    hex_input = "0x051666d3bccc08fd012b2d5fd06252d3197c722778c9"
    cv = deserialize_cv(bytes.fromhex(hex_input[2:]))
    assert cv.type == ClarityType.PrincipalStandard
    assert cv.value.value == hex_input[4:] # Remove "0x" prefix & 05 Principal standard type


def test_deserialize_true_false():
    cv_true = deserialize_cv(bytes.fromhex("03"))
    cv_false = deserialize_cv(bytes.fromhex("04"))
    assert cv_true.type == ClarityType.BoolTrue
    assert cv_false.type == ClarityType.BoolFalse


def test_deserialize_buffer():
    hex_input = "0200000003616263"  # buffer(3) "abc"
    cv = deserialize_cv(bytes.fromhex(hex_input))
    assert cv.type == ClarityType.Buffer
    assert cv.value == b"abc"


def test_deserialize_response_ok():
    hex_input = "07010000000000000000000000000000002a"  # (ok u42)
    cv = deserialize_cv(bytes.fromhex(hex_input))
    assert cv.type == ClarityType.ResponseOk
    assert cv.value.value == 42


def test_deserialize_response_err():
    hex_input = "08010000000000000000000000000000002a"  # (err u42)
    cv = deserialize_cv(bytes.fromhex(hex_input))
    assert cv.type == ClarityType.ResponseErr
    assert cv.value.value == 42


def test_deserialize_optional_some():
    hex_input = "0a010000000000000000000000000000002a"  # (some u42)
    cv = deserialize_cv(bytes.fromhex(hex_input))
    assert cv.type == ClarityType.OptionalSome
    assert cv.value.value == 42


def test_deserialize_optional_none():
    hex_input = "0909"  # (none)
    cv = deserialize_cv(bytes.fromhex(hex_input))
    assert cv.type == ClarityType.OptionalNone
    assert cv.value is None


def test_deserialize_list():
    hex_input = "0b00000002010000000000000000000000000000002a010000000000000000000000000000002b"  # (list [u42, u43])
    cv = deserialize_cv(bytes.fromhex(hex_input))
    assert cv.type == ClarityType.List
    assert len(cv.list) == 2
    assert cv.list[0].value == 42
    assert cv.list[1].value == 43


def test_deserialize_tuple():
    hex_input = "0c000000010161010000000000000000000000000000002a"  # (tuple {"a": u42})
    cv = deserialize_cv(bytes.fromhex(hex_input))
    assert cv.type == ClarityType.Tuple
    assert "a" in cv.value
    assert cv.value["a"].value == 42


def test_deserialize_ascii_string():
    hex_input = "0d00000007636c6172697479"  # (string-ascii "clarity")
    cv = deserialize_cv(bytes.fromhex(hex_input))
    assert cv.type == ClarityType.StringASCII
    assert cv.value == "clarity"


def test_deserialize_utf8_string():
    hex_input = "0e00000010436f6769746f2c206572676f2073756d"  # (string-utf8 "Cogito, ergo sum")
    cv = deserialize_cv(bytes.fromhex(hex_input))
    assert cv.type == ClarityType.StringUTF8
    assert cv.data == "Cogito, ergo sum"