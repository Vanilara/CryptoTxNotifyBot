from integrations.base import BaseRequestSender
from integrations.models import Request, HTTPMethod, ResponseWithRequest
from core.networks import Network, Networks
from schemas.wallets import BalanceDTO


class BalanceGetterERC(BaseRequestSender):
    network = Networks.ERC20.value

    def __init__(self):
        super().__init__(
            base_url = self._make_endpoint_url(network = self.network)
        )

    def _make_requests(self, addresses: list[str]) -> list[Request]:
        return [Request(
            method = HTTPMethod.POST,
            url = self.base_url,
            json_payload = {
                "id": 67,
                "jsonrpc": "2.0",
                "method": "qn_getWalletTokenBalance",
                "params": [{
                    "wallet": address,
                    "contracts": [self.network.smart_contract_address]
                }]
            }
        ) for address in addresses]

    def _handle_response(
        self, response: ResponseWithRequest
    ) -> BalanceDTO:
        address = response.request.json_payload['params'][0]['wallet']
        if response.status == 400:
            return BalanceDTO(
                address = address,
                is_validated = False,
                network = self.network.abbr
            )
        else:
            is_validated, amount = True, 0
            if len(response.data['result']['result']) < 1:
                is_validated = False
            else:
                amount_str = response.data['result']['result'][0]['totalBalance']
                amount = round(int(amount_str) / 1000000, 2)
            return BalanceDTO(
                address = address,
                is_validated = is_validated,
                amount = amount,
                network = self.network.abbr
            )

    async def take_balances(self, addresses: list[str]) -> list[BalanceDTO]:
        requests = self._make_requests(addresses)
        responses = await self._send_group_requests(requests, limit = None)
        results = [self._handle_response(response) for response in responses]
        return results