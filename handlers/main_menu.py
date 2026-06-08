import logging

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config import ADMIN_USERNAME
from texts import *
from keyboards.main_menu import main_menu_keyboard
from keyboards.inline import cases_keyboard, demo_end_keyboard
from handlers.order import start_order

main_router = Router()


@main_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(MAIN_MENU_TITLE, reply_markup=main_menu_keyboard)


@main_router.message(F.text == PRICING)
async def pricing_handler(message: Message):
    await message.answer(PRICING_TEXT, reply_markup=main_menu_keyboard)


@main_router.message(F.text == CONTACT)
async def contact_handler(message: Message):
    text = CONTACT_TEXT.replace("{admin_username}", ADMIN_USERNAME)
    await message.answer(text, reply_markup=main_menu_keyboard)


@main_router.message(F.text == CASES)
async def cases_handler(message: Message):
    await message.answer(CASES_TITLE, reply_markup=cases_keyboard())


@main_router.message(F.text == ORDER_BOT)
async def order_handler(message: Message, state: FSMContext):
    await start_order(message, state)


@main_router.callback_query(F.data == "order_want")
async def order_want_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await start_order(callback.message, state)


@main_router.callback_query(F.data == "order_contact")
async def order_contact_callback(callback: CallbackQuery):
    text = CONTACT_TEXT.replace("{admin_username}", ADMIN_USERNAME)
    await callback.message.edit_text(text, reply_markup=demo_end_keyboard())


@main_router.callback_query(F.data == "back_menu")
async def back_to_menu(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(MAIN_MENU_TITLE, reply_markup=main_menu_keyboard)
