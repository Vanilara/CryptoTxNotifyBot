from core.networks import Network
from core.config import settings
from core.exceptions import ExpressionUnvalidated, NoSuchAlert, NoSuchWebhook
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
        webhook_id = self.webhook_ids_handler.get_webhook_id(self.network.abbr)
        await self.alerts_manager.update(
            alert_id = webhook_id,
            expression = expression.hashed
        )
        self.logger.info(f'Updated webhook {webhook_id}')
            
