import logging

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from config import BOT_TOKEN, ADMIN_CHAT_ID
from texts import *
from keyboards.main_menu import main_menu_keyboard
from states.order import OrderForm

order_router = Router()


async def start_order(message: Message, state: FSMContext):
    await state.set_state(OrderForm.name)
    await message.answer(ORDER_NAME, reply_markup=main_menu_keyboard)


@order_router.message(StateFilter(OrderForm.name))
async def process_name(message: Message, state: FSMContext):
    if len(message.text.strip()) < 1:
        await message.answer("Пожалуйста, введите ваше имя:")
        return
    await state.update_data(name=message.text.strip())
    await state.set_state(OrderForm.contact)
    await message.answer(ORDER_CONTACT)


@order_router.message(StateFilter(OrderForm.contact))
async def process_contact(message: Message, state: FSMContext):
    if len(message.text.strip()) < 1:
        await message.answer("Пожалуйста, укажите ваш Telegram:")
        return
    await state.update_data(contact=message.text.strip())
    await state.set_state(OrderForm.description)
    await message.answer(ORDER_DESC)


@order_router.message(StateFilter(OrderForm.description))
async def process_description(message: Message, state: FSMContext):
    if len(message.text.strip()) < 1:
        await message.answer("Пожалуйста, опишите вашу задачу:")
        return
    await state.update_data(description=message.text.strip())

    data = await state.get_data()
    await state.clear()

    await message.answer(ORDER_DONE, reply_markup=main_menu_keyboard)

    await notify_admin(data, message.from_user.username or message.from_user.id)


async def notify_admin(data: dict, user_identifier):
    bot = None
    try:
        from aiogram import Bot
        from aiogram.client.default import DefaultBotProperties
        from aiogram.enums import ParseMode

        bot = Bot(
            token=BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )

        text = ORDER_ADMIN_TEXT.format(
            name=data.get("name", "—"),
            tg=data.get("contact", user_identifier),
            desc=data.get("description", "—"),
        )

        if ADMIN_CHAT_ID and ADMIN_CHAT_ID > 0:
            await bot.send_message(chat_id=ADMIN_CHAT_ID, text=text)
            logging.info(f"Order sent to admin (chat_id={ADMIN_CHAT_ID})")
        else:
            logging.warning("ADMIN_CHAT_ID is not set or invalid")

    except Exception as e:
        logging.error(f"Failed to send order to admin: {e}")
    finally:
        if bot:
            await bot.session.close()
