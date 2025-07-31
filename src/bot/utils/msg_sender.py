from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from core.config import settings
from core.networks import Networks
from schemas.transactions import NotificationDTO
from utils.logger_setter import Loggable



class TransactionSender(Loggable):
    async def handle_notifications(self, notification: NotificationDTO):
        network = Networks.get_by_abbr(notification.network)
        message = (
            f'You {notification.transfer_type.value} <b>{notification.amount} USDT</b>\n\n'
            f'{notification.other_wallet_role}\n'
            f'<pre>{notification.other_address}</pre>\n\n'
            f'Wallet <b>{notification.wallet_name}</b> - <i>{network.user_name}</i>\n'
            f'<pre>{notification.user_address}</pre>\n\n'
            f'⏱ {notification.time} UTC'
        )
        button = [[InlineKeyboardButton(text = f'View on {network.scaner_name}', url = notification.link)]]
        await self._send_messages(notification.chat_ids, message, InlineKeyboardMarkup(inline_keyboard = button))
        

    async def _send_messages(self, ids, text, buttons):
        bot = Bot(token=settings.bot.TOKEN)
        for id in ids:
            try:
                await bot.send_message(chat_id=id, text=text, reply_markup=buttons, parse_mode='html')
            except Exception as e:
                self.logger.error(f"While sending to {id} message {text}", exc_info=True)
        await bot.session.close()