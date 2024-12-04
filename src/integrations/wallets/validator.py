from typing import Any

from integrations.base import BaseRequestSender
from integrations.models import HTTPMethod
from core.networks import Network


class WalletValidator(BaseRequestSender):
    def __init__(self, network: Network):
        super().__init__(
            base_url = self._make_endpoint_url(network = network)
        )
        self.network = network
    
    def _make_request_on_network(self, address: str) -> tuple[dict[str, Any], str]:
        match self.network.abbr:
            case 'ERC':
                json_payload = {
                    "method": "eth_getAccount",
                    "params": [
                        address, "latest"
                    ],
                    "id": 1,
                    "jsonrpc": "2.0"
                }
                extra_url = ''
            case 'TRC':
                json_payload = {
                    'address': address,
                    'visible': True
                }
                extra_url = '/wallet/getaccount'
            case _:
                raise ValueError()
        return json_payload, extra_url

    def _handle_response(self, data):
        is_validated = False
        match self.network.abbr:
            case 'ERC':
                if 'result' in data:
                    is_validated = True
            case 'TRC':
                if 'address' in data:
                    is_validated = True
        return is_validated
            

    async def check_wallet(self, address: str) -> bool:
        json_payload, extra_url = self._make_request_on_network(address)
        res = await self._send_request(
            HTTPMethod.POST,
            json = json_payload,
            extra_url = extra_url
        )
        if res.status == 200 and self._handle_response(await res.json()):
            return True
        return False
