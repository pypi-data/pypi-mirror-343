# pyclarity-values

A Python library for working with [Clarity](https://docs.stacks.co/docs/clarity/) smart contract values on the [Stacks blockchain](https://stacks.co).
Supports full serialization/deserialization of all Clarity types, including principals, lists, tuples, strings, optional and response types.

---

## Features

- ✅ Deserialize raw Clarity bytes
- ✅ Serialize Clarity types into bytes
- ✅ Conversion between human-readable principals and hash160
- ✅ Support for all Clarity types
- ✅ Minimal and type-safe core

---

## Installation

```bash
pip install pyclarity-values
```

Or from source:

```bash
git clone https://github.com/allbridge-io/pyclarity-values.git
cd pyclarity-values
pip install .
```

---

## Usage

```python
from clarity import deserialize_cv, serialize_cv, principal_cv, address_to_string
from clarity import UIntCV, StandardPrincipalCV, Address

# Deserialize UInt
cv = deserialize_cv(bytes.fromhex("0100000000000000000000000000002a"))
print(cv.value)  # 42

# Serialize back
print(serialize_cv(cv).hex())  # 0100000000000000000000000000002a

# Principals
addr = Address(type=1, version=22, hash160="c34898bb416add50607c973b125560d31c07fd1b")
cv = StandardPrincipalCV(addr)
print(serialize_cv(cv).hex())  # 0516c348...
print(address_to_string(addr))  # SP31MH65V85NDTM30FJBKP4JNC39HR1ZX3CRW9Z97

# From principal string
cv = principal_cv("SP31MH65V85NDTM30FJBKP4JNC39HR1ZX3CRW9Z97.bridge")
print(serialize_cv(cv).hex())
```

---

## Supported Clarity Types

- `IntCV`, `UIntCV`
- `BufferCV`, `StringAsciiCV`, `StringUtf8CV`
- `BooleanCV`
- `OptionalCV`, `SomeCV`, `NoneCV`
- `ResponseOkCV`, `ResponseErrorCV`
- `ListCV`, `TupleCV`
- `StandardPrincipalCV`, `ContractPrincipalCV`

---

## License

MIT

