from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


class AddWalletFSM(StatesGroup):
    set_name = State()
    set_network = State()
    set_address = State()

class RenameWalletFSM(StatesGroup):
    set_name = State()