from core.networks import Network, Networks
from core.config import settings
from core.exceptions import NoSuchAlert
from integrations.base import BaseRequestSender
from integrations.models import HTTPMethod


class AlertsManager(BaseRequestSender):
    def __init__(self, network: Network):
        super().__init__(
            base_url=settings.integrations.QUICKNODE_API_URL + '/streams/rest/v1/streams',
            base_headers = {
                'Content-Type': 'application/json', 
                'x-api-key': settings.integrations.QUICKNODE_API_KEY
            }
        )
        self.name_base_part = 'CryptoNotifier-'
        self.network = network

    async def validate_expression(self, expression: str) -> bool:
        response = await self._send_request(
            HTTPMethod.POST,
            extra_url = '/validate',
            json = {
                'expression': expression,
                'network': self.network.quicknode_name,
            }
        )
        self.logger.debug(f'Validated: {await response.text()}')
        return True if await response.text() == 'true' else False

    async def update(self, alert_id: str, expression: str) -> None:
        response = await self._send_request(
            HTTPMethod.PATCH,
            extra_url = f'/{alert_id}',
            json = {
                'filter_function': expression
            }
        )
        if response.status == 404:
            raise NoSuchAlert