from core.networks import Network
from core.config import settings
from core.exceptions import NotOneDestination, TooManyDestinations
from integrations.transactions.alerts import AlertsManager
from integrations.transactions.destinations import DestinationManager
from utils.logger_setter import Loggable


class DestinationService(Loggable):
    """Works with destinations to set and handle webhooks"""
    def __init__(self):
        self.destination_manager = DestinationManager()
        self.webhook_url = settings.app.WEBHOOK_URL
        super().__init__()

    async def create_if_not(self) -> None:
        await self.delete_wrong_url_destinations()
        destinations = await self.destination_manager.get_service_dests()
        if len(destinations) == 0:
            await self.destination_manager.create(self.webhook_url)

    async def get_main_id(self):
        destinations = await self.destination_manager.get_service_dests()
        if len(destinations) != 1:
            raise NotOneDestination(f'Must be 1 service dest, here is {len(destinations)}: {destinations}')
        return destinations[0].id

    async def delete_wrong_url_destinations(self) -> None:
        destinations = await self.destination_manager.get_service_dests()
        for destination in destinations:
            if self.webhook_url != destination.url:
                await self.destination_manager.delete_by_id(destination.id)

    
            
        