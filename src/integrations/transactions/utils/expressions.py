from pydantic import BaseModel
from core.networks import Network
from utils.hasher.common import Hasher
import logging


class Expression(BaseModel):
    hashed: str
    readable: str
    

class ExpressionMaker:
    transfer_event = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'

    @classmethod
    def make_expression(
        cls, network: Network, addresses: list
    ) -> Expression:
        base_expression = f"""
            tx_logs_address == '{network.smart_contract_address}' &&
            tx_logs_topic0 == '{cls.transfer_event}'
        """
        converted_addresses =[
            network.addresses_converter.convert_to_evm(address) for address in addresses
        ]
        if len(converted_addresses) == 1:
            address = f"'{converted_addresses[0]}'"
            addresses_expression = f"""
                && (
                    tx_logs_topic1 == {address} ||
                    tx_logs_topic2 == {address} ||
                    tx_from == {address}
                )
            """
        else:
            evm_addresses = ', '.join(f"'{addr}'" for addr in converted_addresses)
            addresses_expression = f"""
                && (
                    tx_logs_topic1 in ({evm_addresses}) ||
                    tx_logs_topic2 in ({evm_addresses}) ||
                    tx_from in ({evm_addresses})
                )
            """
        expression = base_expression + addresses_expression
        clear_expression = " ".join(expression.split())
        hashed_expression = Hasher.hash_to_base_64(clear_expression)
        return Expression(
            hashed = hashed_expression,
            readable = clear_expression
        )