import pytest

from src.services.user_service import UserService
from src.schemas.users import UserPostDTO
from src.db.core.unit_of_work import UnitOfWork




@pytest.mark.asyncio
class TestUserService:
    async def test_insert_if_not_exist(self, unit_of_work: UnitOfWork, user1, user2):
        user_service = UserService(unit_of_work)
        for user in [user1, user2, user2]:
            await user_service.insert_if_not_exist(user)

        async with unit_of_work as uow:
            assert len(await unit_of_work.users.select_all()) == 2