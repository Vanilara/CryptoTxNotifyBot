from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from core.networks import Networks
from db.core.unit_of_work import UnitOfWork
from services.wallet_service import WalletService
from services.group_service import GroupService
from schemas.groups import GroupOfWalletPostDTO
from bot.resources.keyboards import ReplyKBs, InlineKBs
from bot.resources.text_answers import TextMsgs
from bot.resources.callbacks_factory import (SpecifiedWalletCB, WalletsCB, 
    ChangeGroupNotifsCB, ShowGroupsWalletCB)
from bot.resources.states import AddWalletFSM, RenameWalletFSM


r = Router()

@r.callback_query(SpecifiedWalletCB.filter(F.action == 'show'))
async def show_wallets(
    callback: CallbackQuery, 
    callback_data: SpecifiedWalletCB, 
    uow: UnitOfWork = UnitOfWork()
):
    wallet = await WalletService(uow).get_wallet(callback_data.id)
    await callback.message.edit_text( 
        text = TextMsgs.wallet(wallet),
        reply_markup = InlineKBs.wallet(wallet)
    )

@r.callback_query(WalletsCB.filter(F.action == 'add'))
async def add_wallet(
    callback: CallbackQuery, 
    state: FSMContext
):
    await state.set_state(AddWalletFSM.set_name)
    await callback.message.answer(
        text = TextMsgs.WALLET_ADD_NAME,
        reply_markup = ReplyKBs.cancelling_kb
    )
    await callback.message.delete()

@r.callback_query(SpecifiedWalletCB.filter(F.action == 'rename'))
async def rename_wallet(
    callback: CallbackQuery, 
    state: FSMContext, 
    callback_data: SpecifiedWalletCB, 
    uow: UnitOfWork = UnitOfWork()
):
    wallet = await WalletService(uow).get_wallet(callback_data.id)
    await state.update_data(id = callback_data.id)
    await state.set_state(RenameWalletFSM.set_name)
    await callback.message.answer(
        text = TextMsgs.wallet_rename_set(wallet.name),
        reply_markup = ReplyKBs.cancelling_kb
    )
    await callback.message.delete()

@r.callback_query(SpecifiedWalletCB.filter(F.action == 'delete'))
async def delete_wallet(
    callback: CallbackQuery, 
    callback_data: SpecifiedWalletCB, 
    uow: UnitOfWork = UnitOfWork()
):
    wallet = await WalletService(uow).delete_wallet(callback_data.id)
    user_network = Networks.get_by_abbr(wallet.network).user_name
    await callback.message.edit_text(
        text = TextMsgs.wallet_deleted(wallet.name, user_network)
    )

@r.callback_query(SpecifiedWalletCB.filter(F.action == 'notificate'))
async def change_wallet_notifications(
    callback: CallbackQuery, 
    callback_data: SpecifiedWalletCB, 
    uow: UnitOfWork = UnitOfWork()
):
    wallet = await WalletService(uow).update_notifications(callback_data.id)
    await callback.message.edit_text(
        text = TextMsgs.wallet(wallet), 
        reply_markup = InlineKBs.wallet(wallet)
    )

@r.callback_query(ShowGroupsWalletCB.filter(F.action == 'groups'))
async def manage_wallet_groups(
    callback: CallbackQuery, 
    callback_data: ShowGroupsWalletCB, 
    uow: UnitOfWork = UnitOfWork()
):
    wallet_groups = await GroupService(uow).get_groups_marked_by_wallet(
        wallet_id = callback_data.id,
        user_id = callback.from_user.id
    )
    reply_markup = InlineKBs.wallet_groups(wallet_id = callback_data.id, groups = wallet_groups)
    if callback_data.has_to_render_text:
        await callback.message.edit_text(
            text = TextMsgs.GROUPS_INFO, 
            reply_markup = reply_markup
        )
    else:
        await callback.message.edit_reply_markup(
            reply_markup = reply_markup
        )

@r.callback_query(ChangeGroupNotifsCB.filter())
async def remove_group_notification(
    callback: CallbackQuery,
    callback_data: ChangeGroupNotifsCB,
    uow: UnitOfWork = UnitOfWork()
):
    groups = await GroupService(uow).group_change_notification(GroupOfWalletPostDTO(
        user_id=callback.from_user.id,
        **callback_data.model_dump()
    ))
    await callback.message.edit_reply_markup(
        reply_markup = InlineKBs.wallet_groups(
            wallet_id = callback_data.wallet_id,
            groups = groups
        )
    )

    