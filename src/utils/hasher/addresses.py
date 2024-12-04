from abc import ABC, abstractmethod
import base58
import hashlib


class AbstractConverter(ABC):
    @classmethod
    @abstractmethod
    def convert_to_evm(cls, address: str) -> str:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def convert_from_evm(cls, address: str) -> str:
        raise NotImplementedError()
    
class TRC20Converter(AbstractConverter):
    @staticmethod
    def _sha256(msg):
        return hashlib.sha256(bytes.fromhex(msg)).hexdigest()

    @classmethod
    def convert_to_evm(cls, address: str) -> str:
        return f'0x{'0'*24}' + base58.b58decode(address).hex()[2:-8]

    @classmethod
    def convert_from_evm(cls, address: str) -> str:
        if address.startswith(f'0x{24*"0"}'):
            addr = '41' + address[26:]
        else:
            addr = '41' + address[2:]
        doubleSha256 = cls._sha256(cls._sha256(addr))
        checkSum = doubleSha256[:8]
        _address = bytes.fromhex(addr + checkSum)
        return base58.b58encode(_address).decode()
    
class ERC20Converter(AbstractConverter):
    @classmethod
    def convert_to_evm(cls, address: str) -> str:
        return f'0x{'0'*24}{address[2:]}'
    
    @classmethod
    def convert_from_evm(cls, address: str) -> str:
        if address.startswith(f'0x{24*'0'}'):
            return f'0x{address[26:]}'
        return address


    