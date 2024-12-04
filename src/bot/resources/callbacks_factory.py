from aiogram.filters.callback_data import CallbackData


class WalletsCB(CallbackData, prefix='wallet'):
    action: str

class SpecifiedWalletCB(WalletsCB, prefix='wallet'):
    id: int

class ShowGroupsWalletCB(SpecifiedWalletCB, prefix='wallet'):
    has_to_render_text: bool = True

class ChangeGroupNotifsCB(CallbackData, prefix='wallet_group'):
    group_id: int
    wallet_id: int
    value: bool