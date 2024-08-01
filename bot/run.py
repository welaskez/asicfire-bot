from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from middlewares import DatabaseMiddleware

from db.engine import session_maker, create_db

from redis.asyncio import Redis

from handlers import routers
from filters import ChatType

import asyncio
import logging
import config

redis = Redis(host="localhost", port=6379)

bot = Bot(
    token=config.BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML,
        link_preview_is_disabled=False,
    ),
)
dp = Dispatcher(r=redis)


async def on_startup(bot: Bot):
    await create_db()
    logging.info("Bot has started")


async def on_shutdown(bot: Bot):
    await redis.aclose()
    logging.info("Bot has finished the job!")


async def main():
    dp.message.filter(ChatType(chat_types=["private"]))
    dp.include_routers(*routers)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(DatabaseMiddleware(session_pool=session_maker))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(f"{config.BASE_DIR.parent}/bot.log")],
    )
    asyncio.run(main())
