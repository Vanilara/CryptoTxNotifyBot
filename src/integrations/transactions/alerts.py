from core.networks import Network, Networks
from core.config import settings
from core.exceptions import NoSuchAlert
from integrations.base import BaseRequestSender
from integrations.models import HTTPMethod


class AlertsManager(BaseRequestSender):
    def __init__(self, network: Network):
        super().__init__(
            base_url=settings.integrations.QUICKNODE_API_URL + '/quickalerts/rest/v1/notifications',
            base_headers = {
                'Content-Type': 'application/json', 
                'x-api-key': settings.integrations.QUICKNODE_API_KEY
            }
        )
        self.name_base_part = 'CryptoNotifier-'
        self.network = network

    async def get_all(self) -> list[dict]:
        networks_abbr = [network.value.abbr for network in Networks]
        response = await self._send_request(HTTPMethod.GET)
        data = await response.json()
        res_webhooks = []
        for webhook in data:
            if webhook['name'] == f'{self.name_base_part}{networks_abbr}':
                res_webhooks.append(webhook)
        return res_webhooks
    
    async def delete_by_id(self, alert_id: str) -> None:
        await self._send_request(
            HTTPMethod.DELETE, 
            extra_url = f'/{alert_id}'
        )

    async def create(self, expression: str, destination_id: str) -> dict:
        response = await self._send_request(
            HTTPMethod.POST,
            json = {
                'name': f'{self.name_base_part}{self.network.abbr}',
                'expression': expression,
                'network': self.network.quicknode_name,
                'destinationIds': [destination_id]
            }
        )
        data = await response.json()
        return data
    
    async def validate_expression(self, expression: str) -> bool:
        response = await self._send_request(
            HTTPMethod.POST,
            extra_url = '/validate',
            json = {
                'expression': expression,
                'network': self.network.quicknode_name,
            }
        )
        return True if await response.text() == 'true' else False

    async def update(self, alert_id: str, expression: str) -> None:
        response = await self._send_request(
            HTTPMethod.PATCH,
            extra_url = f'/{alert_id}',
            json = {
                'expression': expression
            }
        )
        if response.status == 404:
            raise NoSuchAlert
        data = await response.json()