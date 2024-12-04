from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

from itertools import batched

from core.networks import Networks
from bot.resources.callbacks_factory import (SpecifiedWalletCB, WalletsCB, 
    ChangeGroupNotifsCB, ShowGroupsWalletCB)
from schemas.wallets import WalletDTO
from schemas.groups import GroupOfWalletDTO
    

class ReplyKBs:
    @staticmethod
    def _build(kb: list[list[KeyboardButton]]) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True
        )
    
    @staticmethod
    def _button(text: str) -> KeyboardButton:
        return KeyboardButton(text = text)
    
    cancel_text = "❌ Cancel"

    main_menu = _build([[_button("💾 Wallets"), _button("💰 Balances")]])
    cancelling_kb = _build([[_button(cancel_text)]])

    @classmethod
    def adding_wallet_choose_net(cls):
        return cls._build([
            [cls._button(network.value.user_name) for network in Networks],
            [cls._button(cls.cancel_text)]
        ])

class InlineKBs:
    @classmethod
    def bot_link(cls, bot_username) -> InlineKeyboardMarkup:
        return cls._build([[cls._url_button(
            text = 'Open private chat',
            url = f'tg://resolve?domain={bot_username}'
        )]])

    @classmethod
    def wallets(cls, wallets: list[WalletDTO]) -> InlineKeyboardMarkup:
        kb = []
        for wallet_group in batched(wallets, 2):
            kb.append([cls._button(
                f'⚙️ {wallet.name}', SpecifiedWalletCB(action='show', id=wallet.id)
            ) for wallet in wallet_group ])
        kb.append([cls._button('➕ Add new wallet', WalletsCB(action = 'add'))])
        return cls._build(kb)
    
    @classmethod
    def wallet(cls, wallet: WalletDTO) -> InlineKeyboardMarkup:
        notification_button = ('🔕 Disable notifications', SpecifiedWalletCB(action='notificate', id=wallet.id))
        if not wallet.has_notifications:
            notification_button = ('🔔 Enable notifications', SpecifiedWalletCB(action='notificate', id=wallet.id))

        kb = [[
            cls._button('✏️ Rename', SpecifiedWalletCB(action='rename', id=wallet.id)), 
            cls._button('❌ Delete', SpecifiedWalletCB(action='delete', id=wallet.id))
        ], [cls._button(*notification_button)], [
            cls._button('👥 Manage group chats', ShowGroupsWalletCB(action='groups', id=wallet.id))
        ]]
        return cls._build(kb)
    
    @classmethod
    def wallet_groups(cls, wallet_id: int, groups: list[GroupOfWalletDTO]) -> InlineKeyboardMarkup:
        kb = []
        for row in batched(groups, 2):
            kb.append([cls._button(
                text = f'■ {group.title}' if group.has_notifications else f'□ {group.title}',
                callback_data = ChangeGroupNotifsCB(
                    group_id = group.group_id, 
                    value = not group.has_notifications,
                    wallet_id = wallet_id
                )
            ) for group in row])
        kb.append([
            cls._button(
                text = '⬅️ Back',
                callback_data = SpecifiedWalletCB(action = 'show', id = wallet_id)
            ),
            cls._button(
                text = '🔄 Update group list',
                callback_data = ShowGroupsWalletCB(
                    action = 'groups', id = wallet_id, has_to_render_text = False
                )
            ),
        ])
        return cls._build(kb)
    
    @classmethod
    def _build(cls, kb: list[list[InlineKeyboardButton]]) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=kb)
    
    @classmethod
    def _button(cls, text: str, callback_data: CallbackData) -> InlineKeyboardButton:
        return InlineKeyboardButton(text = text, callback_data = callback_data.pack())
    
    @classmethod
    def _url_button(cls, text: str, url: str) -> InlineKeyboardButton:
        return InlineKeyboardButton(text = text, url = url) 