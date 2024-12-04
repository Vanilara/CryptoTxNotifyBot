from core.networks import Network
from core.config import settings
from core.exceptions import ExpressionUnvalidated, NoSuchAlert, NoSuchWebhook
from services.destination_service import DestinationService
from integrations.transactions.alerts import AlertsManager
from integrations.transactions.utils.expressions import ExpressionMaker
from utils.files.state_files_handler import WebhookIdsHandler
from utils.logger_setter import Loggable


class WebhookService(Loggable):
    """Works with alerts to set and handle webhooks"""
    def __init__(self, network: Network):
        self.network = network
        self.alerts_manager = AlertsManager(network)
        self.quicknode_state_file = settings.paths.QUICKNODE_STATE_FILE
        self.webhook_ids_handler = WebhookIdsHandler(self.quicknode_state_file)
        super().__init__()

    async def update_webhook_addresses(self, addresses: list[str]):
        expression = ExpressionMaker.make_expression(self.network, addresses)
        self.logger.info(f'Made expression updating webhook {expression.readable}')
        if not await self.alerts_manager.validate_expression(expression.hashed):
            raise ExpressionUnvalidated(f'{expression} not validated for {self.network.abbr}')
        await self._update_or_create_webhook(expression.hashed)

    async def delete_webhook(self):
        webhook_id = self.webhook_ids_handler.get_webhook_id(self.network.abbr)
        if webhook_id is not None:
            await self.alerts_manager.delete_by_id(webhook_id)
            self.webhook_ids_handler.delete_webhook_id(self.network.abbr)
            self.logger.info(f'Deleted webhook {webhook_id}')

    async def _update_or_create_webhook(self, expression: str) -> None:
        webhook_id = self.webhook_ids_handler.get_webhook_id(self.network.abbr)
        if webhook_id is None:
            self.logger.info(f'Not found webhook {self.network} in state')
            await self._create_if_not_exists(expression)
        else:
            await self._update_if_exists(webhook_id, expression)

    async def _create_webhook(self, expression: str) -> str:
        webhook = await self.alerts_manager.create(
            expression = expression,
            destination_id = await DestinationService().get_main_id()
        )
        webhook_id = webhook['id']
        self.webhook_ids_handler.save_webhook_id(webhook_id, self.network.abbr)
        self.logger.info(f'Created webhook {webhook}')
        return webhook_id
    
    async def _create_if_not_exists(self, expression: str):
        has_to_create = True
        exists_webhooks = await self.alerts_manager.get_all()
        for webhook in exists_webhooks:
            if webhook['network'] == self.network.quicknode_name:
                self.logger.warning(f'Find webhook {self.network} in Quicknode, not in state')
                self.webhook_ids_handler.save_webhook_id(webhook['id'], self.network.abbr)
                await self._update_if_exists(webhook['id'], expression)
                has_to_create = False
        if has_to_create:
            webhook_id = await self._create_webhook(expression)

    async def _update_if_exists(self, webhook_id: str, expression: str):
        try:
            await self.alerts_manager.update(
                alert_id = webhook_id,
                expression = expression
            )
        except NoSuchAlert:
            self.logger.warning(f'Found webhook in state but not in external api: {webhook_id}')
            await self.delete_webhook()
            await self._update_or_create_webhook(expression)
        else:
            self.logger.info(f'Updated webhook {webhook_id}')
            
