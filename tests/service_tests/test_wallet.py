import pytest

from src.core.networks import Networks
from src.services.wallet_service import WalletService
from src.services.user_service import UserService
from src.services.balance_service import BalanceService
from src.services.webhook_service import WebhookService
from src.db.core.unit_of_work import UnitOfWork
from src.schemas.wallets import WalletPostDTO
from src.schemas.users import UserPostDTO
from src.utils import logger_setter
from src.services.destination_service import DestinationService
import logging



async def remove_wallets(unit_of_work: UnitOfWork) -> None:
    async with unit_of_work as uow:
        wallets = await uow.wallets.select_all()
    for wallet in wallets:
        await WalletService(unit_of_work).delete_wallet(wallet.id)
    async with unit_of_work as uow:
        assert len(await uow.wallets.select_all()) == 0

async def delete_old_webhooks_and_create_dest(unit_of_work):
    for network in Networks:
        try:
            await WebhookService(network.value).delete_webhook()
        except ValueError:
            pass
    await DestinationService().create_if_not()

@pytest.mark.asyncio
class TestBalanceService:
    async def test_add_and_delete_wallet(
        self, user1: UserPostDTO, trc_addresses: list[str], erc_addresses: list[str],
        unit_of_work: UnitOfWork
    ):
        await delete_old_webhooks_and_create_dest(unit_of_work)
        await remove_wallets(unit_of_work)

        await UserService(unit_of_work).insert_if_not_exist(user1)
        wallet_ids = []
        for network, addresses in zip(('TRC', 'ERC'), (trc_addresses, erc_addresses)):
            for address in addresses:
                wallet_id = await WalletService(unit_of_work).add_wallet(WalletPostDTO(
                    user_id = user1.user_id,
                    name = 'TestWallet',
                    network = network,
                    address = address
                ))
                wallet_ids.append(wallet_id)

        # async with unit_of_work as uow:
        #     assert len(await uow.wallets.select_all()) == len(trc_addresses) + len(erc_addresses)

        # balances = await BalanceService(unit_of_work).get_user_balances(user1.user_id)
            # logging.getLogger(__name__).info(balances)

        

        

