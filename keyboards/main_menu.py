from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from texts import ORDER_BOT, CASES, PRICING, CONTACT

main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=ORDER_BOT)],
        [KeyboardButton(text=CASES)],
        [KeyboardButton(text=PRICING)],
        [KeyboardButton(text=CONTACT)],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите раздел меню..."
)
