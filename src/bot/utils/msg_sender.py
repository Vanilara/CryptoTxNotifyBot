from aiogram import Bot

from core.config import settings
from core.networks import Networks
from schemas.transactions import NotificationDTO
from utils.logger_setter import Loggable



class TransactionSender(Loggable):
    async def handle_notifications(self, notification: NotificationDTO):
        network = Networks.get_by_abbr(notification.network).user_name
        message = (
            f'You {notification.transfer_type.value} <b>{notification.amount} USDT</b>\n\n'
            f'{notification.other_wallet_role}\n'
            f'<pre>{notification.other_address}</pre>\n\n'
            f'Wallet <b>{notification.wallet_name}</b> - <i>{network}</i>\n'
            f'<pre>{notification.user_address}</pre>\n\n'
            f'Balance: {notification.balance.format_to_msg()}'
        )
        await self._send_messages(notification.chat_ids, message)
        

    @staticmethod
    async def _send_messages(ids, text):
        bot = Bot(token=settings.bot.TOKEN)
        for id in ids:
            await bot.send_message(chat_id = id, text = text, parse_mode='html')
        await bot.session.close()