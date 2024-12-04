from aiogram import Router, F
from aiogram.types import Message, User
from aiogram.filters import Command

from db.core.unit_of_work import UnitOfWork
from schemas.users import UserPostDTO
from services.user_service import UserService
from services.balance_service import BalanceService
from services.wallet_service import WalletService
from bot.resources.keyboards import ReplyKBs
from bot.resources.text_answers import TextMsgs
from bot.resources.filters import UserMsgFilter, GroupMsgFilter
from bot.resources.keyboards import InlineKBs


r = Router()


@r.message(Command('start'), UserMsgFilter())
async def register_user(msg: Message, user: User, uow: UnitOfWork = UnitOfWork()):
    await UserService(uow).insert_if_not_exist(UserPostDTO(
        user_id = user.id,
        username = user.username,
        first_name = user.first_name,
    ))
    await msg.answer(
        text = TextMsgs.welcome(user.first_name), 
        reply_markup=ReplyKBs.main_menu
    )

@r.message(Command('balances'), GroupMsgFilter())
async def get_balances_group(msg: Message, uow: UnitOfWork = UnitOfWork()):
    balances = await BalanceService(uow).get_group_balances(msg.chat.id)
    await msg.answer(
        text = TextMsgs.balances(balances)
    )


@r.message(Command('balances'), UserMsgFilter())
@r.message(F.text == ('💰 Balances'), UserMsgFilter())
async def get_balances_user(msg: Message, user: User, uow: UnitOfWork = UnitOfWork()):
    balances = await BalanceService(uow).get_user_balances(user.id)
    await msg.answer(
        text = TextMsgs.balances(balances)
    )

@r.message(F.text == ('💾 Wallets'), UserMsgFilter())
async def get_wallets(msg: Message, user: User, uow: UnitOfWork = UnitOfWork()):
    wallets = await WalletService(uow).get_user_wallets(user.id)
    await msg.answer(
        text=TextMsgs.wallets(wallets), 
        reply_markup=InlineKBs.wallets(wallets)
    )