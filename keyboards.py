from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menuKeyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🚀 Подобрать решение", callback_data="menu_quiz")],
            [InlineKeyboardButton(text="💼 Кейсы", callback_data="menu_cases")],
            [InlineKeyboardButton(text="💰 Цены", callback_data="menu_prices")],
            [InlineKeyboardButton(text="💬 Связаться лично", callback_data="menu_contact")]
        ]
    )


def backKeyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="menu_back")]
        ]
    )


def quiz_step1_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Бизнес", callback_data="quiz_who_business"),
                InlineKeyboardButton(text="Блогер", callback_data="quiz_who_blogger"),
                InlineKeyboardButton(text="Эксперт", callback_data="quiz_who_expert")
            ],
            [
                InlineKeyboardButton(text="Онлайн школа", callback_data="quiz_who_online"),
                InlineKeyboardButton(text="Магазин", callback_data="quiz_who_store"),
                InlineKeyboardButton(text="Специалист", callback_data="quiz_who_specialist")
            ],
            [InlineKeyboardButton(text="Другое ✍️", callback_data="quiz_who_other")]
        ]
    )


def quiz_step2_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Больше заявок", callback_data="quiz_what_leads")],
            [InlineKeyboardButton(text="Автоматизацию", callback_data="quiz_what_automation")],
            [InlineKeyboardButton(text="Продажи", callback_data="quiz_what_sales")],
            [InlineKeyboardButton(text="Запись клиентов", callback_data="quiz_what_booking")],
            [InlineKeyboardButton(text="Базу подписчиков", callback_data="quiz_what_base")],
            [InlineKeyboardButton(text="Прогрев клиентов", callback_data="quiz_what_warmup")],
            [InlineKeyboardButton(text="Другое ✍️", callback_data="quiz_what_other")],
            [InlineKeyboardButton(text="✅ Готово", callback_data="quiz_what_done")]
        ]
    )


def quiz_step3_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Telegram", callback_data="quiz_platform_telegram")],
            [InlineKeyboardButton(text="WhatsApp", callback_data="quiz_platform_whatsapp")],
            [InlineKeyboardButton(text="Telegram + WhatsApp", callback_data="quiz_platform_both")],
            [InlineKeyboardButton(text="Нужна консультация", callback_data="quiz_platform_consult")],
            [InlineKeyboardButton(text="Другое ✍️", callback_data="quiz_platform_other")]
        ]
    )


def quiz_step4_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Приём заявок", callback_data="quiz_func_leads")],
            [InlineKeyboardButton(text="Оплата", callback_data="quiz_func_payment")],
            [InlineKeyboardButton(text="Рассылка", callback_data="quiz_func_mailing")],
            [InlineKeyboardButton(text="CRM", callback_data="quiz_func_crm")],
            [InlineKeyboardButton(text="Лид-магнит", callback_data="quiz_func_magnet")],
            [InlineKeyboardButton(text="AI ответы", callback_data="quiz_func_ai")],
            [InlineKeyboardButton(text="Запись клиентов", callback_data="quiz_func_booking")],
            [InlineKeyboardButton(text="Каталог", callback_data="quiz_func_catalog")],
            [InlineKeyboardButton(text="Другое ✍️", callback_data="quiz_func_other")],
            [InlineKeyboardButton(text="✅ Готово", callback_data="quiz_func_done")]
        ]
    )


def quiz_step5_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="До 15к", callback_data="quiz_budget_15")],
            [InlineKeyboardButton(text="15–30к", callback_data="quiz_budget_30")],
            [InlineKeyboardButton(text="30–70к", callback_data="quiz_budget_70")],
            [InlineKeyboardButton(text="70к+", callback_data="quiz_budget_70plus")],
            [InlineKeyboardButton(text="Нужна оценка", callback_data="quiz_budget_estimate")],
            [InlineKeyboardButton(text="Другое ✍️", callback_data="quiz_budget_other")]
        ]
    )


def quiz_step6_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Срочно", callback_data="quiz_when_urgent")],
            [InlineKeyboardButton(text="3 дня", callback_data="quiz_when_3days")],
            [InlineKeyboardButton(text="Неделя", callback_data="quiz_when_week")],
            [InlineKeyboardButton(text="Месяц", callback_data="quiz_when_month")],
            [InlineKeyboardButton(text="Пока присматриваюсь", callback_data="quiz_when_looking")],
            [InlineKeyboardButton(text="Другое ✍️", callback_data="quiz_when_other")]
        ]
    )


def quiz_step7_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Telegram", callback_data="quiz_contact_telegram")],
            [InlineKeyboardButton(text="WhatsApp", callback_data="quiz_contact_whatsapp")],
            [InlineKeyboardButton(text="Оставить username", callback_data="quiz_contact_username")],
            [InlineKeyboardButton(text="Другое ✍️", callback_data="quiz_contact_other")]
        ]
    )


def after_quiz_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💬 Написать лично", callback_data="menu_contact")],
            [InlineKeyboardButton(text="💰 Узнать стоимость", callback_data="menu_prices")],
            [InlineKeyboardButton(text="🚀 Новая заявка", callback_data="menu_quiz")]
        ]
    )