from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from texts import *

# ============ Сases list ============
def cases_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=CASE_ASTROLOGER, callback_data="case_astrologer"))
    builder.row(InlineKeyboardButton(text=CASE_BEAUTY, callback_data="case_beauty"))
    builder.row(InlineKeyboardButton(text=CASE_STORE, callback_data="case_store"))
    builder.row(InlineKeyboardButton(text=CASE_HR, callback_data="case_hr"))
    builder.row(InlineKeyboardButton(text=CASE_EDU, callback_data="case_edu"))
    return builder.as_markup()

# ============ Astrologer ============
def astro_deck_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=ASTRO_DECK_1, callback_data="astro_deck_1")
    builder.button(text=ASTRO_DECK_2, callback_data="astro_deck_2")
    builder.button(text=ASTRO_DECK_3, callback_data="astro_deck_3")
    builder.adjust(1)
    return builder.as_markup()

def astro_cards_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=ASTRO_CARD_1, callback_data="astro_card_1")
    builder.button(text=ASTRO_CARD_2, callback_data="astro_card_2")
    builder.button(text=ASTRO_CARD_3, callback_data="astro_card_3")
    builder.adjust(3)
    return builder.as_markup()

# ============ Beauty salon ============
def beauty_services_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=BEAUTY_SERVICE_MANICURE, callback_data="beauty_service_manicure")
    builder.button(text=BEAUTY_SERVICE_HAIRCUT, callback_data="beauty_service_haircut")
    builder.button(text=BEAUTY_SERVICE_MAKEUP, callback_data="beauty_service_makeup")
    builder.button(text=BEAUTY_SERVICE_STYLING, callback_data="beauty_service_styling")
    builder.adjust(1)
    return builder.as_markup()

def beauty_masters_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=BEAUTY_MASTER_1, callback_data="beauty_master_1")
    builder.button(text=BEAUTY_MASTER_2, callback_data="beauty_master_2")
    builder.button(text=BEAUTY_MASTER_3, callback_data="beauty_master_3")
    builder.adjust(2)
    return builder.as_markup()

def beauty_dates_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=BEAUTY_DATE_1, callback_data="beauty_date_1")
    builder.button(text=BEAUTY_DATE_2, callback_data="beauty_date_2")
    builder.button(text=BEAUTY_DATE_3, callback_data="beauty_date_3")
    builder.adjust(2)
    return builder.as_markup()

def beauty_confirm_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=BEAUTY_CONFIRM_YES, callback_data="beauty_confirm")
    builder.button(text=BEAUTY_CONFIRM_NO, callback_data="beauty_cancel")
    builder.adjust(2)
    return builder.as_markup()

# ============ Store ============
def store_items_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for item in STORE_ITEMS:
        builder.button(text=f"{item['name']} — {item['price']} ₽", callback_data=f"store_item_{item['id']}")
    builder.adjust(1)
    return builder.as_markup()

def store_item_actions_keyboard(item_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🛒 Добавить в корзину", callback_data=f"store_cart_add_{item_id}")
    builder.button(text="⬅️ К списку", callback_data="store_back")
    builder.adjust(1)
    return builder.as_markup()

def store_cart_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Оформить заказ", callback_data="store_checkout")
    builder.button(text="⬅️ В каталог", callback_data="store_back")
    builder.adjust(1)
    return builder.as_markup()

# ============ HR ============
def hr_vacancies_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=HR_VACANCY_PYTHON, callback_data="hr_vacancy_python")
    builder.button(text=HR_VACANCY_JS, callback_data="hr_vacancy_js")
    builder.button(text=HR_VACANCY_DESIGNER, callback_data="hr_vacancy_designer")
    builder.button(text=HR_VACANCY_PM, callback_data="hr_vacancy_pm")
    builder.adjust(1)
    return builder.as_markup()

def hr_experience_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=HR_EXP_1, callback_data="hr_exp_0")
    builder.button(text=HR_EXP_2, callback_data="hr_exp_1")
    builder.button(text=HR_EXP_3, callback_data="hr_exp_2")
    builder.button(text=HR_EXP_4, callback_data="hr_exp_3")
    builder.adjust(1)
    return builder.as_markup()

def hr_skills_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=HR_SKILL_BACKEND, callback_data="hr_skill_backend")
    builder.button(text=HR_SKILL_FRONTEND, callback_data="hr_skill_frontend")
    builder.button(text=HR_SKILL_DESIGN, callback_data="hr_skill_design")
    builder.button(text=HR_SKILL_MANAGEMENT, callback_data="hr_skill_management")
    builder.adjust(1)
    return builder.as_markup()

def hr_confirm_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=HR_CONFIRM_YES, callback_data="hr_confirm")
    builder.button(text=HR_CONFIRM_NO, callback_data="hr_cancel")
    builder.adjust(2)
    return builder.as_markup()

# ============ Education ============
def edu_lessons_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=EDU_LESSON_PYTHON, callback_data="edu_lesson_python")
    builder.button(text=EDU_LESSON_JS, callback_data="edu_lesson_js")
    builder.button(text=EDU_LESSON_HTML, callback_data="edu_lesson_html")
    builder.adjust(1)
    return builder.as_markup()

def edu_question_keyboard(lesson_key: str, q_index: int) -> InlineKeyboardMarkup:
    questions = EDU_QUESTIONS[lesson_key]
    q_data = questions[q_index]
    builder = InlineKeyboardBuilder()
    for i, opt in enumerate(q_data["options"]):
        builder.button(text=opt, callback_data=f"edu_answer_{lesson_key}_{q_index}_{i}")
    builder.adjust(1)
    return builder.as_markup()

# ============ Post-demo ============
def demo_end_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=DEMO_WANT_BOT, callback_data="order_want")
    builder.button(text=DEMO_CONTACT, callback_data="order_contact")
    builder.adjust(1)
    return builder.as_markup()
