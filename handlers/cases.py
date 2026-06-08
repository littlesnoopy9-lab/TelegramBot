import logging
import random

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from config import ADMIN_USERNAME
from texts import *
from keyboards.inline import (
    astro_deck_keyboard,
    astro_cards_keyboard,
    beauty_services_keyboard,
    beauty_masters_keyboard,
    beauty_dates_keyboard,
    beauty_confirm_keyboard,
    store_items_keyboard,
    store_item_actions_keyboard,
    store_cart_keyboard,
    hr_vacancies_keyboard,
    hr_experience_keyboard,
    hr_skills_keyboard,
    hr_confirm_keyboard,
    edu_lessons_keyboard,
    edu_question_keyboard,
    demo_end_keyboard,
)

cases_router = Router()

# ---------- Temporary storage for user data ----------
# {chat_id: {key: value}}
user_data: dict[int, dict] = {}

STORE_ITEMS_MAP = {item["id"]: item for item in STORE_ITEMS}

HR_EXP_LABELS = [HR_EXP_1, HR_EXP_2, HR_EXP_3, HR_EXP_4]
HR_SKILL_LABELS = {
    "backend": HR_SKILL_BACKEND,
    "frontend": HR_SKILL_FRONTEND,
    "design": HR_SKILL_DESIGN,
    "management": HR_SKILL_MANAGEMENT,
}
HR_VACANCY_LABELS = {
    "python": HR_VACANCY_PYTHON,
    "js": HR_VACANCY_JS,
    "designer": HR_VACANCY_DESIGNER,
    "pm": HR_VACANCY_PM,
}

BEAUTY_SERVICE_LABELS = {
    "manicure": BEAUTY_SERVICE_MANICURE,
    "haircut": BEAUTY_SERVICE_HAIRCUT,
    "makeup": BEAUTY_SERVICE_MAKEUP,
    "styling": BEAUTY_SERVICE_STYLING,
}
BEAUTY_MASTER_LABELS = [BEAUTY_MASTER_1, BEAUTY_MASTER_2, BEAUTY_MASTER_3]
BEAUTY_DATE_LABELS = [BEAUTY_DATE_1, BEAUTY_DATE_2, BEAUTY_DATE_3]

EDU_LESSON_LABELS = {
    "python": EDU_LESSON_PYTHON,
    "js": EDU_LESSON_JS,
    "html": EDU_LESSON_HTML,
}


def _get_user_data(chat_id: int) -> dict:
    if chat_id not in user_data:
        user_data[chat_id] = {}
    return user_data[chat_id]


def _clear_user_data(chat_id: int):
    user_data.pop(chat_id, None)


# ======================================================================
# CASE SELECTION
# ======================================================================
@cases_router.callback_query(F.data.startswith("case_"))
async def case_selection(callback: CallbackQuery):
    case = callback.data.split("_", 1)[1]
    _clear_user_data(callback.from_user.id)

    handlers = {
        "astrologer": start_astrologer,
        "beauty": start_beauty,
        "store": start_store,
        "hr": start_hr,
        "edu": start_edu,
    }

    handler = handlers.get(case)
    if handler:
        await handler(callback)


# ======================================================================
# ASTROLOGER CASE
# ======================================================================
async def start_astrologer(callback: CallbackQuery):
    await callback.message.edit_text(ASTRO_START, reply_markup=astro_deck_keyboard())


@cases_router.callback_query(F.data.startswith("astro_deck_"))
async def astro_deck_chosen(callback: CallbackQuery):
    await callback.message.edit_text(ASTRO_CHOOSE_CARD, reply_markup=astro_cards_keyboard())


@cases_router.callback_query(F.data.startswith("astro_card_"))
async def astro_card_chosen(callback: CallbackQuery):
    result = random.choice(ASTRO_PREDICTIONS)
    text = ASTRO_RESULT.format(result=result)

    builder = InlineKeyboardBuilder()
    builder.button(text=ASTRO_CONSULT, callback_data="astro_consult")
    builder.button(text="⬅️ Заново", callback_data="case_astrologer")
    builder.adjust(1)

    await callback.message.edit_text(text, reply_markup=builder.as_markup())


@cases_router.callback_query(F.data == "astro_consult")
async def astro_consult(callback: CallbackQuery):
    await callback.message.edit_text(
        f"✨ Запись на консультацию — напишите @{ADMIN_USERNAME}",
        reply_markup=demo_end_keyboard(),
    )


# ======================================================================
# BEAUTY SALON CASE
# ======================================================================
async def start_beauty(callback: CallbackQuery):
    _clear_user_data(callback.from_user.id)
    await callback.message.edit_text(BEAUTY_START, reply_markup=beauty_services_keyboard())


@cases_router.callback_query(F.data.startswith("beauty_service_"))
async def beauty_service_chosen(callback: CallbackQuery):
    service_key = callback.data.split("_", 2)[2]
    data = _get_user_data(callback.from_user.id)
    data["service"] = BEAUTY_SERVICE_LABELS.get(service_key, service_key)

    await callback.message.edit_text(BEAUTY_CHOOSE_MASTER, reply_markup=beauty_masters_keyboard())


@cases_router.callback_query(F.data.startswith("beauty_master_"))
async def beauty_master_chosen(callback: CallbackQuery):
    master_idx = int(callback.data.split("_", 2)[2]) - 1
    data = _get_user_data(callback.from_user.id)
    data["master"] = BEAUTY_MASTER_LABELS[master_idx] if 0 <= master_idx < len(BEAUTY_MASTER_LABELS) else "—"

    await callback.message.edit_text(BEAUTY_CHOOSE_DATE, reply_markup=beauty_dates_keyboard())


@cases_router.callback_query(F.data.startswith("beauty_date_"))
async def beauty_date_chosen(callback: CallbackQuery):
    date_idx = int(callback.data.split("_", 2)[2]) - 1
    data = _get_user_data(callback.from_user.id)
    data["date"] = BEAUTY_DATE_LABELS[date_idx] if 0 <= date_idx < len(BEAUTY_DATE_LABELS) else "—"

    text = BEAUTY_CONFIRM_TITLE
    text += BEAUTY_CONFIRM_DETAILS.format(
        service=data.get("service", "—"),
        master=data.get("master", "—"),
        date=data.get("date", "—"),
    )
    text += BEAUTY_CONFIRM_QUESTION

    await callback.message.edit_text(text, reply_markup=beauty_confirm_keyboard())


@cases_router.callback_query(F.data == "beauty_confirm")
async def beauty_confirm(callback: CallbackQuery):
    await callback.message.edit_text(BEAUTY_DONE, reply_markup=demo_end_keyboard())


@cases_router.callback_query(F.data == "beauty_cancel")
async def beauty_cancel(callback: CallbackQuery):
    await callback.message.edit_text(BEAUTY_START, reply_markup=beauty_services_keyboard())


# ======================================================================
# ONLINE STORE CASE
# ======================================================================
async def start_store(callback: CallbackQuery):
    data = _get_user_data(callback.from_user.id)
    data["cart"] = []
    await callback.message.edit_text(STORE_START, reply_markup=store_items_keyboard())


@cases_router.callback_query(F.data.startswith("store_item_"))
async def store_view_item(callback: CallbackQuery):
    item_id = int(callback.data.split("_", 2)[2])
    item = STORE_ITEMS_MAP.get(item_id)
    if not item:
        return

    text = STORE_ITEM_VIEW.format(name=item["name"], desc=item["desc"], price=item["price"])
    await callback.message.edit_text(text, reply_markup=store_item_actions_keyboard(item_id))


@cases_router.callback_query(F.data.startswith("store_cart_add_"))
async def store_add_to_cart(callback: CallbackQuery):
    item_id = int(callback.data.rsplit("_", 1)[1])
    item = STORE_ITEMS_MAP.get(item_id)
    if not item:
        return

    data = _get_user_data(callback.from_user.id)
    data.setdefault("cart", []).append(item_id)

    await callback.answer(STORE_ADDED.format(name=item["name"]), show_alert=False)

    if len(data["cart"]) == 1:
        text = STORE_CART_TITLE + STORE_CART_ITEM.format(name=item["name"], price=item["price"])
        text += STORE_CART_TOTAL.format(total=item["price"])
        text += "\n\nЧто дальше?"
        await callback.message.edit_text(text, reply_markup=store_cart_keyboard())
    else:
        cart = data["cart"]
        total = sum(STORE_ITEMS_MAP[i]["price"] for i in cart)
        lines = []
        for i in cart:
            it = STORE_ITEMS_MAP[i]
            lines.append(STORE_CART_ITEM.format(name=it["name"], price=it["price"]))
        text = STORE_CART_TITLE + "".join(lines) + STORE_CART_TOTAL.format(total=total)
        text += "\n\nЧто дальше?"
        await callback.message.edit_text(text, reply_markup=store_cart_keyboard())


@cases_router.callback_query(F.data == "store_back")
async def store_back(callback: CallbackQuery):
    await callback.message.edit_text(STORE_START, reply_markup=store_items_keyboard())


@cases_router.callback_query(F.data == "store_checkout")
async def store_checkout(callback: CallbackQuery):
    data = _get_user_data(callback.from_user.id)
    cart = data.get("cart", [])
    if not cart:
        await callback.answer(STORE_CART_EMPTY, show_alert=True)
        return

    total = sum(STORE_ITEMS_MAP[i]["price"] for i in cart)
    text = f"✅ <b>Заказ оформлен!</b>\n\nСумма: {total} ₽\n\nСпасибо за покупку!"
    await callback.message.edit_text(text, reply_markup=demo_end_keyboard())


# ======================================================================
# HR BOT CASE
# ======================================================================
async def start_hr(callback: CallbackQuery):
    _clear_user_data(callback.from_user.id)
    await callback.message.edit_text(HR_START, reply_markup=hr_vacancies_keyboard())


@cases_router.callback_query(F.data.startswith("hr_vacancy_"))
async def hr_vacancy_chosen(callback: CallbackQuery):
    vacancy_key = callback.data.split("_", 2)[2]
    data = _get_user_data(callback.from_user.id)
    data["vacancy"] = HR_VACANCY_LABELS.get(vacancy_key, vacancy_key)

    await callback.message.edit_text(HR_EXP_QUESTION, reply_markup=hr_experience_keyboard())


@cases_router.callback_query(F.data.startswith("hr_exp_"))
async def hr_exp_chosen(callback: CallbackQuery):
    exp_idx = int(callback.data.split("_", 2)[2])
    data = _get_user_data(callback.from_user.id)
    data["exp"] = HR_EXP_LABELS[exp_idx] if 0 <= exp_idx < len(HR_EXP_LABELS) else "—"

    await callback.message.edit_text(HR_SKILL_QUESTION, reply_markup=hr_skills_keyboard())


@cases_router.callback_query(F.data.startswith("hr_skill_"))
async def hr_skill_chosen(callback: CallbackQuery):
    skill_key = callback.data.split("_", 2)[2]
    data = _get_user_data(callback.from_user.id)
    data["skill"] = HR_SKILL_LABELS.get(skill_key, skill_key)

    text = HR_CONFIRM_TITLE
    text += HR_CONFIRM_DETAILS.format(
        vacancy=data.get("vacancy", "—"),
        exp=data.get("exp", "—"),
        skill=data.get("skill", "—"),
    )
    text += HR_CONFIRM_QUESTION

    await callback.message.edit_text(text, reply_markup=hr_confirm_keyboard())


@cases_router.callback_query(F.data == "hr_confirm")
async def hr_confirm(callback: CallbackQuery):
    await callback.message.edit_text(HR_DONE, reply_markup=demo_end_keyboard())


@cases_router.callback_query(F.data == "hr_cancel")
async def hr_cancel(callback: CallbackQuery):
    await callback.message.edit_text(HR_START, reply_markup=hr_vacancies_keyboard())


# ======================================================================
# EDUCATIONAL BOT CASE
# ======================================================================
async def start_edu(callback: CallbackQuery):
    _clear_user_data(callback.from_user.id)
    await callback.message.edit_text(EDU_START, reply_markup=edu_lessons_keyboard())


@cases_router.callback_query(F.data.startswith("edu_lesson_"))
async def edu_lesson_chosen(callback: CallbackQuery):
    lesson_key = callback.data.split("_", 2)[2]
    questions = EDU_QUESTIONS.get(lesson_key)
    if not questions:
        return

    data = _get_user_data(callback.from_user.id)
    data["edu_lesson"] = lesson_key
    data["edu_answers"] = []
    data["edu_q_index"] = 0

    await show_edu_question(callback.message, lesson_key, 0)
    await callback.answer()


async def show_edu_question(message, lesson_key: str, q_index: int):
    questions = EDU_QUESTIONS[lesson_key]
    if q_index >= len(questions):
        await show_edu_result(message, lesson_key)
        return

    q_data = questions[q_index]
    text = EDU_TEST_START.format(
        lesson=EDU_LESSON_LABELS.get(lesson_key, lesson_key),
        num=q_index + 1,
        total=len(questions),
    )
    text += EDU_TEST_QUESTION.format(question=q_data["q"])

    # Build keyboard
    builder = InlineKeyboardBuilder()
    for i, opt in enumerate(q_data["options"]):
        builder.button(text=opt, callback_data=f"edu_answer_{lesson_key}_{q_index}_{i}")
    builder.adjust(1)

    await message.edit_text(text, reply_markup=builder.as_markup())


@cases_router.callback_query(F.data.startswith("edu_answer_"))
async def edu_answer_chosen(callback: CallbackQuery):
    parts = callback.data.split("_")
    lesson_key = parts[2]
    q_index = int(parts[3])
    selected = int(parts[4])

    questions = EDU_QUESTIONS.get(lesson_key)
    if not questions:
        return

    data = _get_user_data(callback.from_user.id)
    data.setdefault("edu_answers", []).append({
        "q_index": q_index,
        "selected": selected,
        "correct": questions[q_index]["answer"],
    })

    next_q = q_index + 1
    if next_q < len(questions):
        await show_edu_question(callback.message, lesson_key, next_q)
    else:
        await show_edu_result(callback.message, lesson_key)
    await callback.answer()


async def show_edu_result(message, lesson_key: str):
    questions = EDU_QUESTIONS[lesson_key]
    data = _get_user_data(message.chat.id)
    answers = data.get("edu_answers", [])

    correct_count = sum(
        1 for a in answers if a["selected"] == a["correct"]
    )
    total = len(questions)

    if correct_count == total:
        grade = EDU_GRADE_5
    elif correct_count >= total * 0.66:
        grade = EDU_GRADE_4
    elif correct_count >= total * 0.33:
        grade = EDU_GRADE_3
    else:
        grade = EDU_GRADE_2

    text = EDU_RESULT.format(correct=correct_count, total=total, grade=grade)

    try:
        await message.edit_text(text, reply_markup=demo_end_keyboard())
    except Exception:
        pass
