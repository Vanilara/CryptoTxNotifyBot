import asyncio

from core.networks import Networks
from core.exceptions import DestinationHasAlerts
from db.core.unit_of_work import UnitOfWork
from services.destination_service import DestinationService
from services.webhook_service import WebhookService
from services.wallet_service import WalletService
from utils.logger_setter import starter_logger



async def main():
    """Run's automatically on build. Needed to avoid wrong url webhooks"""
    dest_service = DestinationService()
    try:
        await dest_service.create_if_not()
    except DestinationHasAlerts:
        for network in Networks:
            await WebhookService(network.value).delete_webhook()

        await dest_service.create_if_not()

        for network in Networks:
            addresses = await WalletService(UnitOfWork()).get_addresses_by_network(network.value)
            if len(addresses) != 0:
                await WebhookService(network.value).update_webhook_addresses(addresses)
    starter_logger.info('Initial webhook checking - SUCCESS')
            



if __name__ == '__main__':
    asyncio.run(main())