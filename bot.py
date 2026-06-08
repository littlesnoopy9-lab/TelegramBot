import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from handlers.main_menu import main_router
from handlers.cases import cases_router
from handlers.order import order_router


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


async def main():
    if not BOT_TOKEN:
        logging.error("BOT_TOKEN is not set in .env file")
        return

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()
    dp.include_routers(main_router, cases_router, order_router)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        logging.info("Starting polling...")
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Error during polling: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
