from .common import address_to_string, create_lp_string, utf8_to_bytes, c32address_decode
from .constants import ClarityType, StacksMessageType


# Define Address and LengthPrefixedString classes
class Address:
    def __init__(self, type: int, version: int, hash160: str):
        self.type = type
        self.version = version
        self.hash160 = hash160

    @property
    def value(self):
        return self.hash160


class LengthPrefixedString:
    def __init__(self, type: int, content: str, lengthPrefixBytes: int, maxLengthBytes: int):
        self.type = type
        self.content = content
        self.lengthPrefixBytes = lengthPrefixBytes
        self.maxLengthBytes = maxLengthBytes


# Define PrincipalCV class and its subclasses
class PrincipalCV:
    def __init__(self, type, address):
        self.type = type
        if not isinstance(address, Address):
            self.address = Address(address['type'], address['version'], address['hash160'])
        else:
            self.address = address


    @property
    def value(self):
        return self.address


class StandardPrincipalCV(PrincipalCV):
    def __init__(self, address: Address):
        self.type = ClarityType.PrincipalStandard
        super().__init__(self.type, address)


class ContractPrincipalCV(PrincipalCV):
    def __init__(self, address: Address, contractName: LengthPrefixedString):
        self.type = ClarityType.PrincipalContract
        self.contract_name = contractName
        super().__init__(self.type, address)


# Define utility functions
def principal_to_string(principal: PrincipalCV) -> str:
    if isinstance(principal, StandardPrincipalCV):
        return address_to_string(principal.address)
    elif isinstance(principal, ContractPrincipalCV):
        address_str = address_to_string(principal.address)
        return f"{address_str}.{principal.contract_name.content}"
    else:
        raise ValueError(f"Unexpected principal data: {principal}")


def principal_cv(principal: str) -> PrincipalCV:
    if "." in principal:
        address_str, contract_name = principal.split(".")
        return contract_principal_cv(address_str, contract_name)
    else:
        return standard_principal_cv(principal)


def create_address(c32AddressString: str) -> Address:
    addressData = c32address_decode(c32AddressString)
    return Address(StacksMessageType.Address, addressData[0], addressData[1])


def standard_principal_cv(addressString: str) -> StandardPrincipalCV:
    addr = create_address(addressString)
    return StandardPrincipalCV(addr)


def standard_principal_cv_from_address(address: Address) -> StandardPrincipalCV:
    return StandardPrincipalCV(address)


def contract_principal_cv(addressString: str, contractName: str) -> ContractPrincipalCV:
    addr = create_address(addressString)
    length_prefixed_contract_name = create_lp_string(contractName)
    return contract_principal_cv_from_address(addr, length_prefixed_contract_name)


def contract_principal_cv_from_address(address: Address, contractName: LengthPrefixedString) -> ContractPrincipalCV:
    if len(utf8_to_bytes(contractName.content)) >= 128:
        raise ValueError('Contract name must be less than 128 bytes')
    return ContractPrincipalCV(address, contractName)


def contract_principal_cv_from_standard(sp: StandardPrincipalCV, contractName: str) -> ContractPrincipalCV:
    length_prefixed_contract_name = create_lp_string(contractName)
    return ContractPrincipalCV(sp.address, length_prefixed_contract_name)
