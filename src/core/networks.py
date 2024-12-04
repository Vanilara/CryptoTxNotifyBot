from pydantic import BaseModel
from enum import Enum

from utils.hasher.addresses import TRC20Converter, ERC20Converter, AbstractConverter


class Network(BaseModel):
    abbr: str
    user_name: str
    quicknode_name: str
    endpoint_quicknode_path: str
    smart_contract_address: str
    addresses_converter: type[AbstractConverter]
    link_scaner: str

    def make_transaction_link(self, hash: str) -> str:
        if self.abbr == Networks.TRC20.value.abbr:
            hash = hash[2:]
        return self.link_scaner + hash
    
class Networks(Enum):
    TRC20 = Network(
        abbr = 'TRC',
        user_name = 'USDT (TRC20)',
        quicknode_name = 'tron-mainnet',
        endpoint_quicknode_path = '.tron-mainnet',
        smart_contract_address = '0xA614F803B6FD780986A42C78EC9C7F77E6DED13C',
        addresses_converter = TRC20Converter,
        link_scaner = 'https://tronscan.org/#/transaction/'
    )
    ERC20 = Network(
        abbr = 'ERC',
        user_name = 'USDT (ERC20)',
        quicknode_name = 'ethereum-mainnet',
        endpoint_quicknode_path = '',
        smart_contract_address = '0xdAC17F958D2ee523a2206206994597C13D831ec7',
        addresses_converter = ERC20Converter,
        link_scaner = 'https://etherscan.io/tx/'
    )

    @classmethod
    def get_by_abbr(cls, abbr: str) -> Network:
        for network in cls:
            if network.value.abbr == abbr:
                return network.value
        raise NotImplemented(f'No network {abbr}')
    
    @classmethod
    def get_by_user_name(cls, user_name: str) -> Network:
        for network in cls:
            if network.value.user_name == user_name:
                return network.value
        raise NotImplemented(f'No network {user_name}')