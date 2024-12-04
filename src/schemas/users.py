from datetime import datetime, timezone

from pydantic import BaseModel


class UserPostDTO(BaseModel):
    user_id: int
    first_name: str
    username: str | None = None
    reg_time: datetime = datetime.now(timezone.utc).replace(tzinfo=None)

class UserDTO(UserPostDTO):
    pass