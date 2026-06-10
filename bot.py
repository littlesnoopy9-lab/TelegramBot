import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from config import BOT_TOKEN, WEBHOOK_URL
from handlers.main_menu import main_router
from handlers.cases import cases_router
from handlers.order import order_router


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


async def on_startup(bot: Bot):
    webhook_path = f"/webhook/{BOT_TOKEN}"
    webhook_url = f"{WEBHOOK_URL}{webhook_path}"
    await bot.set_webhook(webhook_url)
    logging.info(f"Webhook set to {webhook_url}")


async def on_shutdown(bot: Bot):
    await bot.delete_webhook()


async def main():
    if not BOT_TOKEN:
        logging.error("BOT_TOKEN is not set in .env file")
        return

    if not WEBHOOK_URL:
        logging.error("WEBHOOK_URL is not set in .env file")
        return

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()
    dp.include_routers(main_router, cases_router, order_router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    port = int(os.environ.get("PORT", 8080))
    webhook_path = f"/webhook/{BOT_TOKEN}"

    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_requests_handler.register(app, path=webhook_path)
    setup_application(app, dp, bot=bot)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=port)
    logging.info(f"Webhook server running on port {port}")
    await site.start()

    try:
        await asyncio.Event().wait()
    finally:
        await runner.cleanup()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
