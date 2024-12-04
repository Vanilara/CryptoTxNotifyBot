from pydantic import BaseModel


class GroupPostDTO(BaseModel):
    user_id: int
    group_id: int
    title: str

class GroupDTO(GroupPostDTO):
    group_id: int

class GroupOfWalletPostDTO(BaseModel):
    user_id: int
    group_id: int
    wallet_id: int
    value: bool

class GroupOfWalletDTO(BaseModel):
    group_id: int
    title: str
    has_notifications: bool