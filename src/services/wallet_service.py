from db.core.unit_of_work import UnitOfWork
from core.networks import Network, Networks
from core.exceptions import (WalletUnvalidated, WalletDuplicateName, 
    WalletDuplicateAddress, WalletNameTooLong, NoSuchWebhook)
from schemas.wallets import WalletPostDTO, WalletUpdateDTO, WalletDTO
from integrations.wallets.validator import WalletValidator
from services.webhook_service import WebhookService
from utils.logger_setter import Loggable


class WalletService(Loggable):
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        super().__init__()
        
    async def rename_wallet(self, user_id: int, wallet_id: int, wallet_name: str) -> None:
        await self.validate_wallet_name(user_id, wallet_name)
        async with self.uow as uow:
            await uow.wallets.update_one(wallet_id, WalletUpdateDTO(
                name = wallet_name
            ))

    async def update_notifications(self, wallet_id: int) -> WalletDTO:
        async with self.uow as uow:
            wallet = await uow.wallets.select_one_or_raise(id = wallet_id)
            wallet.has_notifications = not wallet.has_notifications
            await uow.wallets.update_one(wallet_id, WalletUpdateDTO(
                has_notifications = wallet.has_notifications
            ))
        return wallet

    async def validate_wallet_name(self, user_id: int, wallet_name: str) -> None:
        if len(wallet_name) > 20:
            raise WalletNameTooLong()
        async with self.uow as uow:
            exist_wallet = await uow.wallets.select_one_or_none(
                user_id = user_id, name = wallet_name
            )
        if exist_wallet != None:
            raise WalletDuplicateName()

    async def get_user_wallets(self, user_id: int) -> list[WalletDTO]:
        async with self.uow as uow:
            user_wallets = await uow.wallets.select_all_by(user_id = user_id)
        return user_wallets
    
    async def get_wallet(self, wallet_id: int) -> WalletDTO:
        async with self.uow as uow:
            wallet = await uow.wallets.select_one_or_raise(id = wallet_id)
        return wallet

    async def add_wallet(self, wallet: WalletPostDTO) -> int:
        network = Networks.get_by_abbr(wallet.network)
        async with self.uow as uow:
            exist_wallets = await uow.wallets.select_all_by(user_id=wallet.user_id)
        if any(x.name == wallet.name for x in exist_wallets):
            raise WalletDuplicateName()
        elif any(x.address == wallet.address for x in exist_wallets):
            raise WalletDuplicateAddress()
        elif not await WalletValidator(network).check_wallet(wallet.address):
            raise WalletUnvalidated()
        
        self.logger.debug(f'Validated wallet {wallet}')

        await self._add_webhook_address(network, wallet.address)
        async with self.uow as uow:
            wallet_db = await uow.wallets.add_one(wallet)
        self.logger.info(f'Added wallet {wallet_db}')
        return wallet_db.id

    async def delete_wallet(self, wallet_id: int) -> WalletDTO:
        async with self.uow as uow:
            wallet = await uow.wallets.select_one_or_raise(id = wallet_id)
            amount_wallets_same_address = len(
                await uow.wallets.select_all_by(address = wallet.address)
            )
        network = Networks.get_by_abbr(wallet.network)
        if amount_wallets_same_address == 1:
            await self._remove_webhook_address(network, wallet.address)
        async with self.uow as uow:
            await uow.wallets.delete_groups_relation_by_wallet(wallet_id)
            await uow.wallets.delete_by(id = wallet_id)
        return wallet

    async def update_wallet(
        self, wallet_id: int, updates: WalletUpdateDTO
    ) -> None:
        async with self.uow as uow:
            await uow.wallets.update_one(id = wallet_id, schema = updates)

    async def _add_webhook_address(self, network: Network, address: str) -> None:
        addresses = await self.get_addresses_by_network(network)
        addresses.append(address)
        await WebhookService(network).update_webhook_addresses(addresses)

    async def _remove_webhook_address(self, network: Network, address: str) -> None:
        webhook_service = WebhookService(network)
        addresses = await self.get_addresses_by_network(network)
        addresses.remove(address)
        if len(addresses) == 0:
            try:
                await webhook_service.delete_webhook()
            except NoSuchWebhook:
                self.logger.warning(f'Tried to remove address {address}, but there is not webhook')
        else:
            await webhook_service.update_webhook_addresses(addresses)

    async def get_addresses_by_network(self, network: Network) -> list[str]:
        async with self.uow as uow:
            existing_wallets = await uow.wallets.select_all_by(
                network=network.abbr
            )
        return list(map(lambda x: x.address, existing_wallets))