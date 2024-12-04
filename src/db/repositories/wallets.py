from sqlalchemy import select, or_, delete
from sqlalchemy.orm import selectinload

from db.models import Wallets, Groups, GroupWallets
from db.core.base_repository import SQLAlchemyRepository
from schemas.wallets import WalletDTO, WalletUpdateDTO
from schemas.groups import GroupDTO


class WalletsRep(SQLAlchemyRepository[Wallets, WalletDTO]):
    model = Wallets
    schema = WalletDTO

    async def delete_groups_relation_by_wallet(self, wallet_id: int) -> None:
        await self.session.execute(
            delete(GroupWallets).filter_by(wallet_id = wallet_id)
        )
        await self.session.commit()

    async def select_by_addresses(self, addresses: list[str]) -> list[WalletDTO]:
        return await self._select_by_stmt(
            select(self.model).filter(
                or_(*[self.model.address.ilike(f'%{address}%') for address in addresses])
            )
        )
    
    async def select_by_address(self, address: str) -> list[WalletDTO]:
        return await self._select_by_stmt(
            select(self.model).filter(
                self.model.address.ilike(f'%{address}%') 
            )
        )
    
    async def get_wallet_groups_ids(self, wallet_id: int) -> list[int]:
        result = await self.session.execute(
            select(self.model).filter_by(id=wallet_id).options(
                selectinload(Wallets.groups)
            )
        )
        groups = result.scalar_one().groups
        return [row.group_id for row in groups]
        


        