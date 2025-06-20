from datetime import datetime
from core.networks import Networks
from core.enums import TransferType
from schemas.wallets import BalanceDTO
from schemas.transactions import TransferDTO, NotificationDTO
from db.core.unit_of_work import UnitOfWork
from utils.hasher.common import EvmHasher
from utils.logger_setter import Loggable
from services.balance_service import BalanceService
from services.group_service import GroupService
from bot.utils.msg_sender import TransactionSender


class TransactionService(Loggable):
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        super().__init__()

    async def handle_transactions(self, logs: dict, time_data: str):
        transfers = self._parse_transaction_logs(logs['logs'])
        
        for transfer in transfers:
            if transfer.amount <= 1:
                self.logger.info('Skip transfer cause of low amout')
                continue
            notifications = await self._handle_tranfser(
                transfer, 
                time = self._format_time(time_data)
            )
            for notification in notifications:
                await TransactionSender().handle_notifications(notification)

    async def _handle_tranfser(
        self, transfer: TransferDTO, time: str
    ) -> list[NotificationDTO]:
        notifications = []
        wallets_all_in_transaction = []
        for address, transfer_type in zip((transfer.addr_to, transfer.addr_from), TransferType):
            if transfer_type == TransferType.Receive:
                user_address, other_address = transfer.addr_to, transfer.addr_from
            elif transfer_type == TransferType.Send:
                user_address, other_address = transfer.addr_from, transfer.addr_to,
            async with self.uow as uow:
                wallets = await uow.wallets.select_by_address(address)
                wallets_all_in_transaction += wallets
                for wallet in filter(lambda x: x.has_notifications, wallets):
                    self.logger.info(f'Found in DB {wallet}')
                    wallet_groups = await uow.wallets.get_wallet_groups_ids(wallet.id)
                    notifications.append(NotificationDTO(
                        chat_ids = wallet_groups + [wallet.user_id],
                        transfer_type = transfer_type,
                        network = transfer.network,
                        amount = transfer.amount,
                        user_address = user_address,
                        other_address = other_address,
                        link = transfer.link,
                        wallet_name = wallet.name,
                        time = time
                    ))
        if len(wallets_all_in_transaction) == 0:
            self.logger.warning('No wallet with this transaction')
        elif len(notifications) == 0:
            self.logger.info('All wallets in transaction are set_notifs = False')
        else:
            self.logger.info(f'Notifications: {notifications}')
        return notifications
        

    def _parse_transaction_logs(self, logs: dict) -> list[TransferDTO]:
        transactions = []
        for log in logs:
            network = None
            for item in Networks:
                if item.value.smart_contract_address.lower() == log['address']:
                    network = item.value
            if network is None:
                continue

            converter = network.addresses_converter
            transactions.append(TransferDTO(
                network = network.abbr,
                addr_from = converter.convert_from_evm(log['topics'][1]),
                addr_to = converter.convert_from_evm(log['topics'][2]),
                amount = round(EvmHasher.decode_int(log['data']) / 1000000, 2),
                link = network.make_transaction_link(log['transactionHash'])
            ))
        self.logger.info(f'Parsed transfers: {transactions}')
        if len(transactions) == 0:
            self.logger.warning(f'Empty transactions fot from {logs}')
        return transactions

    def _format_time(self, data):
        string = ' '.join(data.split(' ')[0:2]).split('.')[0]
        time = datetime.strptime(string, '%Y-%m-%d %H:%M:%S')
        return datetime.strftime(time, '%-d %B %H:%M:%S')