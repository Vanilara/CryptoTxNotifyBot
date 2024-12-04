from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from db.core.base_repository import SQLAlchemyRepository
from db.models import Groups, GroupWallets
from schemas.groups import GroupDTO
from schemas.wallets import WalletDTO
from db.models import Wallets


class GroupsRep(SQLAlchemyRepository[Groups, GroupDTO]):
    model = Groups
    schema = GroupDTO

    async def get_wallets_by_group(
        self, group_id: int
    ) -> list[WalletDTO]:
        group = await self.session.execute(
            select(self.model).filter_by(group_id=group_id).options(
                selectinload(self.model.wallets)
            )
        )
        return [WalletDTO.model_validate(
            wallet, from_attributes=True
        ) for wallet in group.scalar_one().wallets]

    async def delete_wallets_relation_by_group(
        self, group_id: int, user_id: int
    ) -> None:
        await self.session.execute(
            delete(GroupWallets).filter_by(group_id = group_id, user_id = user_id)
        )
        await self.session.commit()

    async def change_group_in_wallet(
        self, group_id: int, user_id: int, wallet_id: int, value: bool
    ) -> None:
        group = await self._select_raw_group(group_id, user_id)
        wallet = await self._select_raw_wallet(wallet_id)
        
        if value and group not in wallet.groups:
            wallet.groups.append(group)
        elif not value and group in wallet.groups:
            wallet.groups.remove(group)
        await self.session.commit()

    async def _select_raw_group(self, group_id: int, user_id: int) -> Groups:
        group = await self.session.execute(
            select(self.model).filter_by(group_id=group_id, user_id=user_id)
        )
        return group.scalar_one()
    
    async def _select_raw_wallet(self, wallet_id: int) -> Wallets:
        wallet = await self.session.execute(
            select(Wallets).filter_by(id=wallet_id).options(
                selectinload(Wallets.groups)
            )
        )
        return wallet.scalar_one()