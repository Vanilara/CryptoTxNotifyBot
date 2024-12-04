from enum import Enum

from core.networks import Network
from core.config import settings
from core.exceptions import DestinationHasAlerts
from integrations.base import BaseRequestSender
from integrations.models import HTTPMethod
from schemas.webhooks import DestinationDTO


class PayloadTypes(Enum):
    MATCHED_TRANSACTIONS = 4
    MATCHED_RECEIPTS = 5

class DestinationManager(BaseRequestSender):
    destination_name = 'CryptoNotifierBot'
    payload_types = PayloadTypes

    def __init__(self):
        super().__init__(
            base_url = settings.integrations.QUICKNODE_API_URL + '/quickalerts/rest/v1/destinations',
            base_headers={
                'x-api-key': settings.integrations.QUICKNODE_API_KEY
            }
        )

    async def get_service_dests(self) -> list[DestinationDTO]:
        """Returns destination ID from Quicknode"""
        destinations = []
        response = await self._send_request(
            HTTPMethod.GET
        )
        for destination in await response.json():
            if destination['name'] == self.destination_name:
                self.logger.debug(f'Got destination ID {destination['id']}')
                destinations.append(DestinationDTO(
                    id = destination['id'],
                    name = destination['name'],
                    url = destination['to']
                ))
        return destinations

    async def create(self, webhook_url: str) -> str:
        """Returns destination ID from Quicknode"""
        response = await self._send_request(
            HTTPMethod.POST,
            json = {
                'name': self.destination_name,
                'to_url': webhook_url,
                'webhook_type': 'POST',
                'service': 'webhook',
                'payload_type': self.payload_types.MATCHED_RECEIPTS.value
            }
        )
        data = await response.json()
        return data['id']

    async def delete_by_id(self, destination_id: str) -> None:
        res = await self._send_request(
            HTTPMethod.DELETE, 
            extra_url = f'/{destination_id}'
        )
        if res.status == 403:
            raise DestinationHasAlerts

    

    
        

