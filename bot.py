import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import config
import database as db
import handlers as h
from keyboards import (
    quiz_step1_keyboard, quiz_step2_keyboard, quiz_step3_keyboard,
    quiz_step4_keyboard, quiz_step5_keyboard, quiz_step6_keyboard, quiz_step7_keyboard,
    main_menuKeyboard, backKeyboard, after_quiz_keyboard
)
from states import QuizStates

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(token=config.TOKEN)
dp = Dispatcher()


def register_handlers():
    # Main commands
    dp.message.register(h.cmd_start, Command(commands=["start"]))
    dp.message.register(h.cmd_admin, Command(commands=["admin"]))
    
    # Menu callbacks
    dp.callback_query.register(h.menu_cases, lambda c: c.data == "menu_cases")
    dp.callback_query.register(h.menu_prices, lambda c: c.data == "menu_prices")
    dp.callback_query.register(h.menu_contact, lambda c: c.data == "menu_contact")
    dp.callback_query.register(h.menu_back, lambda c: c.data == "menu_back")
    
    # Quiz start
    dp.callback_query.register(h.quiz_start, lambda c: c.data == "menu_quiz")
    
    # Quiz step 1 - Who
    dp.callback_query.register(h.quiz_step1, lambda c: c.data and c.data.startswith("quiz_who_"))
    dp.message.register(h.quiz_step1_text, QuizStates.step1_who)
    
    # Quiz step 2 - What wants (multiple)
    dp.callback_query.register(h.quiz_step2, lambda c: c.data and c.data.startswith("quiz_what_"))
    dp.message.register(h.quiz_step2_text, QuizStates.step2_what)
    
    # Quiz step 3 - Platform
    dp.callback_query.register(h.quiz_step3, lambda c: c.data and c.data.startswith("quiz_platform_"))
    dp.message.register(h.quiz_step3_text, QuizStates.step3_where)
    
    # Quiz step 4 - Functions (multiple)
    dp.callback_query.register(h.quiz_step4, lambda c: c.data and c.data.startswith("quiz_func_"))
    dp.message.register(h.quiz_step4_text, QuizStates.step4_funcs)
    
    # Quiz step 5 - Budget
    dp.callback_query.register(h.quiz_step5, lambda c: c.data and c.data.startswith("quiz_budget_"))
    dp.message.register(h.quiz_step5_text, QuizStates.step5_budget)
    
    # Quiz step 6 - When
    dp.callback_query.register(h.quiz_step6, lambda c: c.data and c.data.startswith("quiz_when_"))
    dp.message.register(h.quiz_step6_text, QuizStates.step6_when)
    
    # Quiz step 7 - Contact
    dp.callback_query.register(h.quiz_step7, lambda c: c.data and c.data.startswith("quiz_contact_"))
    dp.message.register(h.quiz_step7_text, QuizStates.step7_contact)


async def on_startup(dispatcher: Dispatcher):
    db.init_db()
    logger.info("Bot started and database initialized!")


async def main():
    dp.startup.register(on_startup)
    register_handlers()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    print("Bot starting...")
    asyncio.run(main())