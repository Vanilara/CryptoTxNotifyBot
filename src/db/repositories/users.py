from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload

from db.models import Users
from db.core.base_repository import SQLAlchemyRepository
from schemas.users import UserDTO
from schemas.groups import GroupDTO


class UsersRep(SQLAlchemyRepository[Users, UserDTO]):
    model = Users
    schema = UserDTO

    async def get_user_groups(self, user_id: int) -> list[GroupDTO]:
        result = await self.session.execute(
            select(self.model).filter_by(user_id=user_id).options(
                selectinload(Users.groups)
            )
        )
        groups = result.scalar_one().groups
        return [
            GroupDTO.model_validate(row, from_attributes=True)
            for row in groups
        ]
        