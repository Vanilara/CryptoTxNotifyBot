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

    async def handle_transactions(self, logs: dict):
        transfers = self._parse_transaction_logs(logs['logs'])
        balances = await self._get_transaction_balances(transfers)
        
        for transfer in transfers:
            notifications = await self._handle_tranfser(transfer, balances)
            self.logger.info(f'Notifications: {notifications}')
            for notification in notifications:
                await TransactionSender().handle_notifications(notification)
        return notifications

    async def _handle_tranfser(
        self, transfer: TransferDTO, balances: list[BalanceDTO]
    ) -> list[NotificationDTO]:
        notifications = []
        for address, transfer_type in zip(transfer.addresses, TransferType):
            self.logger.info(f'Checking {transfer_type}, {address}')
            if transfer_type == TransferType.Receive:
                user_address, other_address = transfer.addr_to, transfer.addr_from
            elif transfer_type == TransferType.Send:
                user_address, other_address = transfer.addr_from, transfer.addr_to,
            async with self.uow as uow:
                wallets = await uow.wallets.select_by_address(address)
                for wallet in wallets:
                    self.logger.info(f'Found in DB {wallet}')
                    wallet_groups = await uow.wallets.get_wallet_groups_ids(wallet.id)
                    balance = list(filter(lambda x: x.address == wallet.address, balances))[0]
                    notifications.append(NotificationDTO(
                        chat_ids = wallet_groups + [wallet.user_id],
                        transfer_type = transfer_type,
                        network = transfer.network,
                        amount = transfer.amount,
                        user_address = user_address,
                        other_address = other_address,
                        link = transfer.link,
                        balance = balance,
                        wallet_name = wallet.name
                    ))
        return notifications
        
    async def _get_transaction_balances(
        self, transfers: list[TransferDTO]
    ) -> list[BalanceDTO]:
        async with self.uow as uow:
            wallets = await uow.wallets.select_by_addresses(
                addresses = [address for transfer in transfers for address in transfer.addresses]
            )
        self.logger.info(f'Wallets from transfer exist in DB: {wallets}')
        balances = await BalanceService(self.uow).get_balances(wallets)
        self.logger.info(f'Balances of exists wallets: {balances}')
        return balances

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