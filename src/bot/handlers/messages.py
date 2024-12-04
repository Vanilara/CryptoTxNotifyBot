from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from db.core.unit_of_work import UnitOfWork

from core.networks import Networks
from bot.resources.keyboards import ReplyKBs
from bot.resources.text_answers import TextMsgs
from bot.resources.states import AddWalletFSM, RenameWalletFSM
from core.exceptions import WalletUnvalidated, WalletDuplicateName, WalletDuplicateAddress, WalletNameTooLong
from services.wallet_service import WalletService
from schemas.wallets import WalletPostDTO


r = Router()



@r.message(F.text == ReplyKBs.cancel_text)
async def cancel(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer(
        text = TextMsgs.CANCEL,
        reply_markup = ReplyKBs.main_menu
    )

@r.message(AddWalletFSM.set_name, F.text)
async def wallet_set_name(msg: Message, state: FSMContext, uow: UnitOfWork = UnitOfWork()):
    try:
        await WalletService(uow).validate_wallet_name(
            user_id = msg.from_user.id, wallet_name = msg.text
        )
    except (WalletDuplicateName, WalletNameTooLong) as e:
        await msg.answer(text = str(e))
        return
    await state.update_data(name = msg.text)
    await state.set_state(AddWalletFSM.set_network)
    await msg.answer(
        text=TextMsgs.WALLET_ADD_NETWORK,
        reply_markup=ReplyKBs.adding_wallet_choose_net()
    )

@r.message(AddWalletFSM.set_network, F.text.in_([net.value.user_name for net in Networks]))
async def wallet_set_network(msg: Message, state: FSMContext):
    await state.update_data(network = Networks.get_by_user_name(msg.text).abbr)
    await state.set_state(AddWalletFSM.set_address)
    await msg.answer(
        text=TextMsgs.WALLET_ADD_ADDRESS,
        reply_markup=ReplyKBs.cancelling_kb
    )      

@r.message(AddWalletFSM.set_address, F.text)
async def wallet_set_address(msg: Message, state: FSMContext, uow: UnitOfWork = UnitOfWork()):
    state_data = await state.get_data()
    try:
        await WalletService(uow).add_wallet(WalletPostDTO(
            **state_data, address = msg.text, user_id = msg.from_user.id
        ))
    except (WalletUnvalidated, WalletDuplicateAddress) as e:
        await msg.answer(text = str(e))
        return
    await state.clear()
    await msg.answer(
        text = TextMsgs.wallet_added(state_data['name']),
        reply_markup = ReplyKBs.main_menu
    )

@r.message(RenameWalletFSM.set_name, F.text)
async def wallet_rename(
    msg: Message,
    state: FSMContext,
    uow: UnitOfWork = UnitOfWork()
):
    try:
        id = await state.get_value('id')
        print(id)
        await WalletService(uow).rename_wallet(
            user_id = msg.from_user.id, 
            wallet_id = id, 
            wallet_name = msg.text
        )
    except (WalletDuplicateName, WalletNameTooLong) as e:
        await msg.answer(text = str(e))
        return
    await state.clear()
    await msg.answer(
        text=TextMsgs.WALLET_RENAMED,
        reply_markup=ReplyKBs.main_menu
    )

        
