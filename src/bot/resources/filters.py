from aiogram.types import Message, User, ChatMemberUpdated, ChatMember
from aiogram.filters import Filter


class UserMsgFilter(Filter):
    async def __call__(self, msg: Message) -> bool | dict[str, User]:
        if msg.chat.type != 'private' or msg.from_user is None:
            return False
        return {"user": msg.from_user}
    
class GroupMsgFilter(Filter):
    async def __call__(self, msg: Message) -> bool:
        if msg.chat.type != 'group':
            return False
        return True

class GroupUpdateFilter(Filter):
    async def __call__(self, update: ChatMemberUpdated) -> bool | dict[str, User | ChatMember]:
        if update.chat.type != 'group' or update.from_user is None:
            return False
        return {"adder_user": update.from_user, 'new_chat_member': update.new_chat_member}