from pyclarity_values import *


def test_serialize_principal_standard():
    addr = Address(type=1, version=22, hash160="c34898bb416add50607c973b125560d31c07fd1b")
    cv = StandardPrincipalCV(addr)
    assert address_to_string(addr) == "SP31MH65V85NDTM30FJBKP4JNC39HR1ZX3CRW9Z97"
    serialized = serialize_cv(cv)
    assert serialized.hex() == "0516c34898bb416add50607c973b125560d31c07fd1b"


def test_serialize_principal_contract():
    addr = Address(type=1, version=22, hash160="c34898bb416add50607c973b125560d31c07fd1b")
    contract_name = create_lp_string("bridge")
    cv = ContractPrincipalCV(addr, contract_name)
    serialized = serialize_cv(cv)
    assert serialized.hex() == "0616c34898bb416add50607c973b125560d31c07fd1b06627269646765"
    assert contract_name.encode("utf-8").hex() in serialized.hex()
    assert address_to_string(addr) == "SP31MH65V85NDTM30FJBKP4JNC39HR1ZX3CRW9Z97"


def test_principal_to_hash():
    principal = "SP31MH65V85NDTM30FJBKP4JNC39HR1ZX3CRW9Z97"
    cv = principal_cv(principal)
    expected = "0516c34898bb416add50607c973b125560d31c07fd1b"
    assert serialize_cv(cv).hex() == expected

    address = Address(
        type=StacksMessageType.Address.value,
        version=AddressVersion.MainnetSingleSig.value,
        hash160=expected[4:]
    )
    assert address_to_string(address) == principal


def test_principal_contract_to_hash():
    principal = "SP31MH65V85NDTM30FJBKP4JNC39HR1ZX3CRW9Z97.bridge"
    cv = principal_cv(principal)
    assert serialize_cv(cv).hex() == "0616c34898bb416add50607c973b125560d31c07fd1b06627269646765"