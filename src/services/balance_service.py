from collections import defaultdict
import asyncio

from db.core.unit_of_work import UnitOfWork
from core.networks import Networks
from schemas.wallets import WalletDTO, BalanceDTO
from integrations.wallets.balances_networks.erc import BalanceGetterERC
from integrations.wallets.balances_networks.trc import BalanceGetterWithLockTRC
from services.wallet_service import WalletService
from utils.logger_setter import Loggable


class BalanceService(Loggable):
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        super().__init__()

    async def get_user_balances(self, user_id: int) -> list[BalanceDTO]:
        user_wallets = await WalletService(self.uow).get_user_wallets(user_id)
        return await self._make_balances(user_wallets)
    
    async def get_group_balances(self, group_id: int) -> list[BalanceDTO]:
        async with self.uow as uow:
            group_wallets = await uow.groups.get_wallets_by_group(group_id)
        return await self._make_balances(group_wallets)
    
    async def get_balances(self, wallets: list[WalletDTO]) -> list[BalanceDTO]:
        addresses_by_network = self._sort_addresses_by_network(wallets)
        trc_addresses = list(addresses_by_network[Networks.TRC20.value.abbr])
        erc_addresses = list(addresses_by_network[Networks.ERC20.value.abbr])

        trc_balances, erc_balances = await asyncio.gather(
            BalanceGetterWithLockTRC().take_balances(trc_addresses),
            BalanceGetterERC().take_balances(erc_addresses),
        )
        balances = trc_balances + erc_balances
        self.logger.info(f'Got balances {balances}')
        return balances
    
    async def _make_balances(self, wallets: list[WalletDTO]) -> list[BalanceDTO]:
        wallet_names = {wallet.address: wallet.name for wallet in wallets}
        balances = await self.get_balances(wallets)
        return [balance.set_name(wallet_names[balance.address]) for balance in balances]

    def _sort_addresses_by_network(
        self, wallets: list[WalletDTO]
    ) -> defaultdict[str, set[str]]:
        addresses_by_network = defaultdict(set)
        for wallet in wallets:
            addresses_by_network[wallet.network].add(wallet.address)
        return addresses_by_network