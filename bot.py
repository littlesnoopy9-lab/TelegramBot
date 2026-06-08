import asyncio
import logging
import os

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


async def health_check():
    port = int(os.environ.get("PORT", 8080))

    async def handler(reader, writer):
        writer.write(b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nOK")
        await writer.drain()
        writer.close()

    server = await asyncio.start_server(handler, host="0.0.0.0", port=port)
    logging.info(f"Health check server running on port {port}")
    async with server:
        await server.serve_forever()


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
        await asyncio.gather(
            dp.start_polling(bot),
            health_check(),
        )
    except Exception as e:
        logging.error(f"Error during polling: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
