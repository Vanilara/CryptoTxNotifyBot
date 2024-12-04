from schemas.groups import GroupPostDTO, GroupOfWalletDTO, GroupOfWalletPostDTO
from db.core.unit_of_work import UnitOfWork
from utils.logger_setter import Loggable


class GroupService(Loggable):
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        super().__init__()

    async def add_group(self, group: GroupPostDTO) -> None:
        async with self.uow as uow:
            await uow.groups.add_one(group)

    async def delete_group(self, user_id: int, group_id: int) -> None:
        async with self.uow as uow:
            await uow.groups.delete_wallets_relation_by_group(
                user_id = user_id, group_id = group_id
            )
            await uow.groups.delete_by(user_id = user_id, group_id = group_id)

    async def group_change_notification(
        self, update: GroupOfWalletPostDTO
    ) -> list[GroupOfWalletDTO]:
        async with self.uow as uow:
            await uow.groups.change_group_in_wallet(**update.model_dump())
            groups = await self.get_groups_marked_by_wallet(
                wallet_id=update.wallet_id, user_id=update.user_id
            )
        return groups

    async def get_groups_marked_by_wallet(
        self, wallet_id: int, user_id: int
    ) -> list[GroupOfWalletDTO]:
        async with self.uow as uow:
            wallet_groups_ids = await uow.wallets.get_wallet_groups_ids(wallet_id)
            user_groups = await uow.users.get_user_groups(user_id)
        return [GroupOfWalletDTO(
            group_id = group.group_id,
            title = group.title,
            has_notifications = group.group_id in wallet_groups_ids
        ) for group in user_groups]