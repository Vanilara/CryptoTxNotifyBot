import asyncio
import time

from core.config import settings
from core.networks import Networks
from integrations.base import BaseRequestSender
from integrations.models import Request, HTTPMethod, ResponseWithRequest
from schemas.wallets import BalanceDTO


class BalanceGetterTRC(BaseRequestSender):
    network = Networks.TRC20.value

    def __init__(self):
        super().__init__(
            base_url = settings.integrations.TRONSCAN_API_URL,
            base_headers={
                "accept": "application/json",
                'TRON-PRO-API-KEY': settings.integrations.TRONSCAN_API_KEY,
                "User-Agent": "Mozilla/5.0",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive"
            }
        )

    def _make_requests(self, addresses: list[str]) -> list[Request]:
        return [Request(
            method = HTTPMethod.GET,
            url = f'{self.base_url}/account/wallet',
            headers=self.base_headers,
            params = {
                'address': address,
                'asset_type': '0'
            }
        ) for address in addresses]

    def _handle_response(
        self, response: ResponseWithRequest
    ) -> BalanceDTO:
        amount = 0
        is_validated = True
        if response.data['data'][0] is None:
            is_validated = False
        else:
            for account in response.data['data']:
                if account['token_abbr'] == 'USDT':
                    amount = account['balance']
                    break
        return BalanceDTO(
            address = response.request.params['address'],
            amount = round(float(amount), 2),
            network = self.network.abbr,
            is_validated = is_validated
        )
    
    async def take_balances(self, addresses: list[str]) -> list[BalanceDTO]:
        requests = self._make_requests(addresses)
        responses = await self._send_group_requests(requests, limit = 1)
        results = [self._handle_response(response) for response in responses]
        return results

class BalanceGetterWithLockTRC:
    lock = asyncio.Lock()
    last_call_time = 0
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(
                BalanceGetterWithLockTRC, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    async def take_balances(
        self, addresses: list[str]
    ) -> list[BalanceDTO]:
        async with self.lock:
            if time.time() - self.last_call_time < 1:
                await asyncio.sleep(1 - (time.time() - self.last_call_time))

            balances = await BalanceGetterTRC().take_balances(addresses)
            self.last_call_time = time.time()
        return balances