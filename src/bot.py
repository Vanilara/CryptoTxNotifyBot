from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

import asyncio

from core.config import settings
from bot.handlers.menues import r as menues_r
from bot.handlers.messages import r as messages_r
from bot.handlers.callbacks import r as callbacks_r
from bot.handlers.updates import r as updates_r


async def main():
    bot = Bot(
        token=settings.bot.TOKEN, 
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    dp.include_routers(menues_r, messages_r, callbacks_r, updates_r)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())