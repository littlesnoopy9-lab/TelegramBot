import logging
import asyncio
from datetime import datetime
from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import config
import keyboards as kb
import database as db
from states import QuizStates

logger = logging.getLogger(__name__)

last_click_time = {}


def check_spam(user_id: int) -> bool:
    now = asyncio.get_event_loop().time()
    if user_id in last_click_time:
        if now - last_click_time[user_id] < 1:
            return True
    last_click_time[user_id] = now
    return False


async def cmd_start(message: Message, state: FSMContext):
    user = message.from_user
    
    if check_spam(user.id):
        await message.answer("Подождите 1 секунду между действиями!")
        return
    
    await state.clear()
    db.add_user(user.id, user.username or "", f"{user.first_name or ''} {user.last_name or ''}".strip())
    
    text = """Привет 👋

Помогаю создать Telegram / WhatsApp бота для продаж, заявок и автоматизации бизнеса.

За 1 минуту подберу лучшее решение под ваш запрос."""
    
    await message.answer(text, reply_markup=kb.main_menuKeyboard())
    await state.set_state(QuizStates.main_menu)


async def menu_cases(callback: CallbackQuery, state: FSMContext):
    if check_spam(callback.from_user.id):
        await callback.answer("Подождите!", show_alert=True)
        return
    
    text = """Примеры решений:

• Бот для записи клиентов
• Лид-магнит бот для блогера
• Бот с оплатой и каталогом
• AI консультант
• Автоворонка продаж"""
    
    await callback.message.edit_text(text, reply_markup=kb.backKeyboard())
    await callback.answer()


async def menu_prices(callback: CallbackQuery, state: FSMContext):
    if check_spam(callback.from_user.id):
        await callback.answer("Подождите!", show_alert=True)
        return
    
    text = """🔹 Start — от 5.000₽
Простой бот / лид-магнит / заявки

🔹 Business — от 25.000₽
Продажи / CRM / оплаты / автоматизация

🔹 Premium — от 70.000₽
AI / сложная логика """
    
    await callback.message.edit_text(text, reply_markup=kb.main_menuKeyboard())
    await callback.answer()


async def menu_contact(callback: CallbackQuery, state: FSMContext):
    if check_spam(callback.from_user.id):
        await callback.answer("Подождите!", show_alert=True)
        return
    
    text = f"Напишите напрямую: @{config.ADMIN_USERNAME}"
    
    await callback.message.edit_text(text, reply_markup=kb.main_menuKeyboard())
    await callback.answer()


async def menu_back(callback: CallbackQuery, state: FSMContext):
    if check_spam(callback.from_user.id):
        await callback.answer("Подождите!", show_alert=True)
        return
    
    text = """Привет 👋

Помогаю создать Telegram / WhatsApp / AI бота для продаж, заявок и автоматизации бизнеса.

За 1 минуту подберу лучшее решение под ваш запрос."""
    
    await callback.message.edit_text(text, reply_markup=kb.main_menuKeyboard())
    await callback.answer()


# Quiz start
async def quiz_start(callback: CallbackQuery, state: FSMContext):
    if check_spam(callback.from_user.id):
        await callback.answer("Подождите!", show_alert=True)
        return
    
    current_state = await state.get_state()
    if current_state and current_state not in ("QuizStates:main_menu", None):
        await callback.answer("Сначала завершите текущую анкету!", show_alert=True)
        return
    
    await state.update_data(
        answers={},
        step=1,
        what_wants=[],
        functions=[]
    )
    
    text = "Шаг 1 из 7\n\nКто вы?"
    await callback.message.edit_text(text, reply_markup=kb.quiz_step1_keyboard())
    await state.set_state(QuizStates.step1_who)
    await callback.answer()


async def quiz_step1(callback: CallbackQuery, state: FSMContext):
    if check_spam(callback.from_user.id):
        await callback.answer("Подождите!", show_alert=True)
        return
    
    data = callback.data
    
    if data == "quiz_who_other":
        await callback.message.answer("Введите ваш ответ:")
        await state.set_state(QuizStates.step1_who)
        return
    
    who_map = {
        "quiz_who_business": "Бизнес",
        "quiz_who_blogger": "Блогер",
        "quiz_who_expert": "Эксперт",
        "quiz_who_online": "Онлайн школа",
        "quiz_who_store": "Магазин",
        "quiz_who_specialist": "Специалист",
    }
    who = who_map.get(data, "Другое")
    
    answers = (await state.get_data()).get("answers", {})
    answers["who_text"] = who
    await state.update_data(answers=answers, step=2)
    
    text = "Шаг 2 из 7\n\nЧто хотите получить?\n(можно выбрать несколько)"
    await callback.message.edit_text(text, reply_markup=kb.quiz_step2_keyboard())
    await state.set_state(QuizStates.step2_what)
    await callback.answer()


async def quiz_step1_text(message: Message, state: FSMContext):
    if check_spam(message.from_user.id):
        await message.answer("Подождите!")
        return
    
    answers = (await state.get_data()).get("answers", {})
    answers["who_text"] = message.text
    await state.update_data(answers=answers, step=2)
    
    await message.answer("Шаг 2 из 7\n\nЧто хотите получить?\n(можно выбрать несколько)", reply_markup=kb.quiz_step2_keyboard())
    await state.set_state(QuizStates.step2_what)


async def quiz_step2(callback: CallbackQuery, state: FSMContext):
    if check_spam(callback.from_user.id):
        await callback.answer("Подождите!", show_alert=True)
        return
    
    data = callback.data
    
    if data == "quiz_what_other":
        await callback.message.answer("Введите ваш ответ:")
        await state.set_state(QuizStates.step2_what)
        return
    
    if data == "quiz_what_done":
        what_wants = (await state.get_data()).get("what_wants", [])
        answers = (await state.get_data()).get("answers", {})
        answers["what_wants"] = ", ".join(what_wants) if what_wants else "Не выбрано"
        await state.update_data(answers=answers, step=3)
        
        text = "Шаг 3 из 7\n\nГде нужен бот?"
        await callback.message.edit_text(text, reply_markup=kb.quiz_step3_keyboard())
        await state.set_state(QuizStates.step3_where)
        await callback.answer()
        return
    
    what_map = {
        "quiz_what_leads": "Больше заявок",
        "quiz_what_automation": "Автоматизацию",
        "quiz_what_sales": "Продажи",
        "quiz_what_booking": "Запись клиентов",
        "quiz_what_base": "Базу подписчиков",
        "quiz_what_warmup": "Прогрев клиентов",
    }
    what = what_map.get(data, "")
    
    if what:
        what_wants = (await state.get_data()).get("what_wants", [])
        if what not in what_wants:
            what_wants.append(what)
        await state.update_data(what_wants=what_wants)
    
    # Показываем снова клавиатуру с текущим статусом
    selected = (await state.get_data()).get("what_wants", [])
    status_text = f"Выбрано: {', '.join(selected)}" if selected else "Пока ничего не выбрано"
    text = f"Шаг 2 из 7\n\nЧто хотите получить?\n(можно выбрать несколько)\n\n{status_text}"
    await callback.message.edit_text(text, reply_markup=kb.quiz_step2_keyboard())
    await callback.answer()


async def quiz_step2_text(message: Message, state: FSMContext):
    if check_spam(message.from_user.id):
        await message.answer("Подождите!")
        return
    
    what_wants = (await state.get_data()).get("what_wants", [])
    what_wants.append(message.text)
    await state.update_data(what_wants=what_wants, step=3)
    
    answers = (await state.get_data()).get("answers", {})
    answers["what_wants"] = ", ".join(what_wants)
    await state.update_data(answers=answers)
    
    await message.answer("Шаг 3 из 7\n\nГде нужен бот?", reply_markup=kb.quiz_step3_keyboard())
    await state.set_state(QuizStates.step3_where)


async def quiz_step3(callback: CallbackQuery, state: FSMContext):
    if check_spam(callback.from_user.id):
        await callback.answer("Подождите!", show_alert=True)
        return
    
    data = callback.data
    
    if data == "quiz_platform_other":
        await callback.message.answer("Введите ваш ответ:")
        await state.set_state(QuizStates.step3_where)
        return
    
    platform_map = {
        "quiz_platform_telegram": "Telegram",
        "quiz_platform_whatsapp": "WhatsApp",
        "quiz_platform_both": "Telegram + WhatsApp",
        "quiz_platform_consult": "Нужна консультация",
    }
    platform = platform_map.get(data, "Другое")
    
    answers = (await state.get_data()).get("answers", {})
    answers["platform"] = platform
    await state.update_data(answers=answers, step=4)
    
    text = "Шаг 4 из 7\n\nКакие функции нужны?\n(можно выбрать несколько)"
    await callback.message.edit_text(text, reply_markup=kb.quiz_step4_keyboard())
    await state.set_state(QuizStates.step4_funcs)
    await callback.answer()


async def quiz_step3_text(message: Message, state: FSMContext):
    if check_spam(message.from_user.id):
        await message.answer("Подождите!")
        return
    
    answers = (await state.get_data()).get("answers", {})
    answers["platform"] = message.text
    await state.update_data(answers=answers, step=4)
    
    await message.answer("Шаг 4 из 7\n\nКакие функции нужны?\n(можно выбрать несколько)", reply_markup=kb.quiz_step4_keyboard())
    await state.set_state(QuizStates.step4_funcs)


async def quiz_step4(callback: CallbackQuery, state: FSMContext):
    if check_spam(callback.from_user.id):
        await callback.answer("Подождите!", show_alert=True)
        return
    
    data = callback.data
    
    if data == "quiz_func_done":
        answers = (await state.get_data()).get("answers", {})
        functions = (await state.get_data()).get("functions", [])
        answers["functions"] = ", ".join(functions) if functions else "Не выбрано"
        await state.update_data(answers=answers, step=5)
        
        text = "Шаг 5 из 7\n\nБюджет"
        await callback.message.edit_text(text, reply_markup=kb.quiz_step5_keyboard())
        await state.set_state(QuizStates.step5_budget)
        await callback.answer()
        return
    
    if data == "quiz_func_other":
        await callback.message.answer("Введите ваш ответ:")
        return
    
    func_map = {
        "quiz_func_leads": "Приём заявок",
        "quiz_func_payment": "Оплата",
        "quiz_func_mailing": "Рассылка",
        "quiz_func_crm": "CRM",
        "quiz_func_magnet": "Лид-магнит",
        "quiz_func_ai": "AI ответы",
        "quiz_func_booking": "Запись клиентов",
        "quiz_func_catalog": "Каталог",
    }
    func = func_map.get(data, "")
    
    if func:
        functions = (await state.get_data()).get("functions", [])
        if func not in functions:
            functions.append(func)
        await state.update_data(functions=functions)
    
    # Показываем снова клавиатуру
    selected = (await state.get_data()).get("functions", [])
    status_text = f"Выбрано: {', '.join(selected)}" if selected else "Пока ничего не выбрано"
    text = f"Шаг 4 из 7\n\nКакие функции нужны?\n(можно выбрать несколько)\n\n{status_text}"
    await callback.message.edit_text(text, reply_markup=kb.quiz_step4_keyboard())
    await callback.answer()


async def quiz_step4_text(message: Message, state: FSMContext):
    if check_spam(message.from_user.id):
        await message.answer("Подождите!")
        return
    
    functions = (await state.get_data()).get("functions", [])
    functions.append(message.text)
    await state.update_data(functions=functions)
    
    await message.answer("Нажмите ✅ Готово когда выберите все функции:", reply_markup=kb.quiz_step4_keyboard())


async def quiz_step5(callback: CallbackQuery, state: FSMContext):
    if check_spam(callback.from_user.id):
        await callback.answer("Подождите!", show_alert=True)
        return
    
    data = callback.data
    
    if data == "quiz_budget_other":
        await callback.message.answer("Введите ваш ответ:")
        return
    
    budget_map = {
        "quiz_budget_15": "До 15к",
        "quiz_budget_30": "15–30к",
        "quiz_budget_70": "30–70к",
        "quiz_budget_70plus": "70к+",
        "quiz_budget_estimate": "Нужна оценка",
    }
    budget = budget_map.get(data, "Другое")
    
    answers = (await state.get_data()).get("answers", {})
    answers["budget"] = budget
    await state.update_data(answers=answers, step=6)
    
    text = "Шаг 6 из 7\n\nКогда нужен запуск?"
    await callback.message.edit_text(text, reply_markup=kb.quiz_step6_keyboard())
    await state.set_state(QuizStates.step6_when)
    await callback.answer()


async def quiz_step5_text(message: Message, state: FSMContext):
    if check_spam(message.from_user.id):
        await message.answer("Подождите!")
        return
    
    answers = (await state.get_data()).get("answers", {})
    answers["budget"] = message.text
    await state.update_data(answers=answers, step=6)
    
    await message.answer("Шаг 6 из 7\n\nКогда нужен запуск?", reply_markup=kb.quiz_step6_keyboard())
    await state.set_state(QuizStates.step6_when)


async def quiz_step6(callback: CallbackQuery, state: FSMContext):
    if check_spam(callback.from_user.id):
        await callback.answer("Подождите!", show_alert=True)
        return
    
    data = callback.data
    
    if data == "quiz_when_other":
        await callback.message.answer("Введите ваш ответ:")
        return
    
    when_map = {
        "quiz_when_urgent": "Срочно",
        "quiz_when_3days": "3 дня",
        "quiz_when_week": "Неделя",
        "quiz_when_month": "Месяц",
        "quiz_when_looking": "Пока присматриваюсь",
    }
    when_launch = when_map.get(data, "Другое")
    
    answers = (await state.get_data()).get("answers", {})
    answers["when_launch"] = when_launch
    await state.update_data(answers=answers, step=7)
    
    text = "Шаг 7 из 7\n\nКак с Вами связаться?"
    await callback.message.edit_text(text, reply_markup=kb.quiz_step7_keyboard())
    await state.set_state(QuizStates.step7_contact)
    await callback.answer()


async def quiz_step6_text(message: Message, state: FSMContext):
    if check_spam(message.from_user.id):
        await message.answer("Подождите!")
        return
    
    answers = (await state.get_data()).get("answers", {})
    answers["when_launch"] = message.text
    await state.update_data(answers=answers, step=7)
    
    await message.answer("Шаг 7 из 7\n\nКак связаться?", reply_markup=kb.quiz_step7_keyboard())
    await state.set_state(QuizStates.step7_contact)


async def quiz_step7(callback: CallbackQuery, state: FSMContext):
    if check_spam(callback.from_user.id):
        await callback.answer("Подождите!", show_alert=True)
        return
    
    data = callback.data
    
    if data == "quiz_contact_other":
        await callback.message.answer("Введ��те ваш ответ:")
        return
    
    contact_map = {
        "quiz_contact_telegram": "Telegram",
        "quiz_contact_whatsapp": "WhatsApp",
        "quiz_contact_username": "Оставить username",
    }
    contact = contact_map.get(data, "Другое")
    
    user = callback.from_user
    answers = (await state.get_data()).get("answers", {})
    answers["contact"] = contact
    
    app_data = {
        "telegram_id": user.id,
        "who_text": answers.get("who_text", ""),
        "what_wants": answers.get("what_wants", ""),
        "platform": answers.get("platform", ""),
        "functions": answers.get("functions", ""),
        "budget": answers.get("budget", ""),
        "when_launch": answers.get("when_launch", ""),
        "contact": answers.get("contact", ""),
    }
    
    app_id = db.save_application(app_data)
    
    admin_text = f"""Новая заявка 🔥

ID: {app_id}
Имя: {user.first_name or ''} {user.last_name or ''}
Username: @{user.username or 'нет'}

Кто: {answers.get('who_text', '')}
Цель: {answers.get('what_wants', '')}
Платформа: {answers.get('platform', '')}
Функции: {answers.get('functions', '')}
Бюджет: {answers.get('budget', '')}
Сроки: {answers.get('when_launch', '')}
Контакт: {answers.get('contact', '')}

Дата: {datetime.now().strftime('%Y-%m-%d %H:%M')}"""
    
    await callback.bot.send_message(config.ADMIN_CHAT_ID, admin_text)
    
    await callback.message.edit_text(
        "Спасибо 👌\n\nУже вижу, какое решение вам подойдет.\n\nСвяжусь с вами в ближайшее время.",
        reply_markup=kb.after_quiz_keyboard()
    )
    await state.clear()
    await callback.answer()


async def quiz_step7_text(message: Message, state: FSMContext):
    if check_spam(message.from_user.id):
        await message.answer("Подождите!")
        return
    
    user = message.from_user
    answers = (await state.get_data()).get("answers", {})
    answers["contact"] = message.text
    
    what_wants = (await state.get_data()).get("what_wants", [])
    if what_wants:
        answers["what_wants"] = ", ".join(what_wants)
    
    app_data = {
        "telegram_id": user.id,
        "who_text": answers.get("who_text", ""),
        "what_wants": answers.get("what_wants", ""),
        "platform": answers.get("platform", ""),
        "functions": answers.get("functions", ""),
        "budget": answers.get("budget", ""),
        "when_launch": answers.get("when_launch", ""),
        "contact": answers.get("contact", ""),
    }
    
    app_id = db.save_application(app_data)
    
    admin_text = f"""Новая заявка 🔥

ID: {app_id}
Имя: {user.first_name or ''} {user.last_name or ''}
Username: @{user.username or 'нет'}

Кто: {answers.get('who_text', '')}
Цель: {answers.get('what_wants', '')}
Платформа: {answers.get('platform', '')}
Функции: {answers.get('functions', '')}
Бюджет: {answers.get('budget', '')}
Сроки: {answers.get('when_launch', '')}
Контакт: {answers.get('contact', '')}

Дата: {datetime.now().strftime('%Y-%m-%d %H:%M')}"""
    
    await message.bot.send_message(config.ADMIN_CHAT_ID, admin_text)
    
    await message.answer(
        "Спасибо 👌\n\nУже вижу, какое решение вам подойдет.\n\nСвяжусь с вами в ближайшее время.",
        reply_markup=kb.after_quiz_keyboard()
    )
    await state.clear()


async def cmd_admin(message: Message, state: FSMContext):
    if message.from_user.id != config.ADMIN_CHAT_ID:
        return
    
    users = db.get_user_count()
    apps = db.get_application_count()
    today = db.get_today_application_count()
    
    text = f"""📊 Статистика

👥 Всего пользователей: {users}
📝 Всего заявок: {apps}
📅 Заявок сегодня: {today}"""
    
    await message.answer(text)
