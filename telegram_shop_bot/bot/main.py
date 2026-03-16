import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from bot.database import db

from bot.handlers import user_handlers, payment_handlers, purchase_handlers, admin_handlers
from bot.config import API_TOKEN

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(
        token=API_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())
    db.init_db()

    dp.include_router(user_handlers.router)
    dp.include_router(payment_handlers.router)
    dp.include_router(purchase_handlers.router)
    dp.include_router(admin_handlers.router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
