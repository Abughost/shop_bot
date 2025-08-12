import asyncio
import logging
import sys

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.i18n import FSMI18nMiddleware

from bot.handlers import *
from bot.utils.dispatcher import TOKEN


async def main() -> None:
    i18n = I18n(path="locales", default_locale="en", domain="messages")
    middleware = FSMI18nMiddleware(i18n)
    dp.update.outer_middleware(middleware)
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())