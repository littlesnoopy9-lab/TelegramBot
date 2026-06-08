from aiogram.fsm.state import StatesGroup, State


class OrderForm(StatesGroup):
    name = State()
    contact = State()
    description = State()
