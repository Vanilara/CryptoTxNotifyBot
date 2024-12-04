from aiogram import Router, F
from aiogram.types import User, ChatMemberUpdated

from db.core.unit_of_work import UnitOfWork
from schemas.groups import GroupPostDTO
from services.group_service import GroupService
from bot.resources.text_answers import TextMsgs
from bot.resources.filters import GroupUpdateFilter
from bot.resources.keyboards import InlineKBs


r = Router()

@r.my_chat_member(GroupUpdateFilter(), F.new_chat_member.status == 'member')
async def bot_added_to_group(update: ChatMemberUpdated, adder_user: User, uow: UnitOfWork = UnitOfWork()):
    bot_info = await update.bot.get_me()
    await GroupService(uow).add_group(GroupPostDTO(
        user_id = adder_user.id,
        group_id = update.chat.id,
        title = update.chat.title
    ))
    await update.answer(
        text = TextMsgs.ADDED_TO_GROUP,
        reply_markup = InlineKBs.bot_link(bot_info.username)
    )

@r.my_chat_member(GroupUpdateFilter(), F.new_chat_member.status == 'left')
async def bot_deleted_from_group(update: ChatMemberUpdated, adder_user: User, uow: UnitOfWork = UnitOfWork()):
    await GroupService(uow).delete_group(
        user_id = adder_user.id,
        group_id = update.chat.id,
    )
