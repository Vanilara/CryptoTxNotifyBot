from db.core.unit_of_work import UnitOfWork
from schemas.users import UserPostDTO


class UserService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def insert_if_not_exist(self, user: UserPostDTO) -> None:
        async with self.uow as uow:
            if await uow.users.select_one_or_none(user_id=user.user_id) is None:
                await uow.users.add_one(user)
        
        

    