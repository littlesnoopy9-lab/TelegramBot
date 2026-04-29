$path = "C:\Telegram"
$botCode = @'
import os
import json
import sqlite3
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.filters import Command, Text
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

if not TOKEN:
    raise SystemExit("Please set TELEGRAM_BOT_TOKEN environment variable.")

if not ADMIN_CHAT_ID:
    raise SystemExit("Please set ADMIN_CHAT_ID environment variable (chat ID for admin).")
try:
    ADMIN_CHAT_ID = int(ADMIN_CHAT_ID)
except ValueError:
    raise SystemExit("ADMIN_CHAT_ID must be an integer.")

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=storage)

DB_PATH = os.path.join(os.getcwd(), "bot_requests.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            full_name TEXT,
            role TEXT,
            answers TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_request(record: dict) -> int:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO requests (user_id, username, full_name, role, answers) VALUES (?, ?, ?, ?, ?)",
        (record["user_id"], record["username"], record["full_name"], record["role"], record["answers"])
    )
    last_id = cur.lastrowid
    conn.commit()
    conn.close()
    return last_id

class RequestStates(StatesGroup):
    role = State()
    traffic = State()
    lead_magnet = State()
    free_offer = State()
    product_sale = State()
    warmup = State()
    contact = State()
    niche = State()
    bot_purpose = State()
    functions = State()
    budget = State()
    contact_biz = State()

def role_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    kb.row(
        InlineKeyboardButton("Biznes", callback_data="role_business"),
        InlineKeyboardButton("Bloger", callback_data="role_blogger"),
        InlineKeyboardButton("Ekspert", callback_data="role_expert")
    )
    kb.row(
        InlineKeyboardButton("Onlayn shkola", callback_data="role_online"),
        InlineKeyboardButton("Magazin", callback_data="role_store"),
        InlineKeyboardButton("Drugoe", callback_data="role_other")
    )
    return kb

def human_role(role_key: str) -> str:
    mapping = {
        "business": "Biznes",
        "blogger": "Bloger",
        "expert": "Ekspert",
        "online": "Onlayn shkola",
        "store": "Magazin",
        "other": "Drugoe",
    }
    return mapping.get(role_key, role_key)

def build_admin_summary(rec_id: int, user_data: dict, role: str, answers: dict) -> str:
    lines = [f"Zayavka #{rec_id}", f"Klient: {user_data.get('full_name')} (@{user_data.get('username', '')})", f"Rol: {role}"]
    lines.append("Otvetu:")
    lines.append(json.dumps(answers, ensure_ascii=False, indent=2))
    lines.append(f"ID zayavki: {rec_id}")
    return "\n".join(lines)

@dp.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Dobro pozhalovat! Oformite zayavku na sozdaniye bota. Kto u?", reply_markup=role_keyboard())
    await state.set_state(RequestStates.role)

@dp.callback_query(Text(startswith="role_"))
async def on_role(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    role_key = callback.data.split("_")[1]
    human = human_role(role_key)
    await state.update_data(role=human)
    if role_key in ("blogger", "expert"):
        await callback.message.edit_text("Otkuda traffic?")
        await state.set_state(RequestStates.traffic)
    else:
        await callback.message.edit_text("Kakaya niche?")
        await state.set_state(RequestStates.niche)

@dp.message(state=RequestStates.traffic)
async def on_traffic(message: Message, state: FSMContext):
    await state.update_data(traffic=message.text)
    await message.answer("Nuzhen lid-magnit?")
    await state.set_state(RequestStates.lead_magnet)

@dp.message(state=RequestStates.lead_magnet)
async def on_lead_magnet(message: Message, state: FSMContext):
    await state.update_data(lead_magnet=message.text)
    await message.answer("Chto otdaete besplatno?")
    await state.set_state(RequestStates.free_offer)

@dp.message(state=RequestStates.free_offer)
async def on_free_offer(message: Message, state: FSMContext):
    await state.update_data(free_offer=message.text)
    await message.answer("Est li product na prodazhu?")
    await state.set_state(RequestStates.product_sale)

@dp.message(state=RequestStates.product_sale)
async def on_product_sale(message: Message, state: FSMContext):
    await state.update_data(product_sale=message.text)
    await message.answer("Nuzhen progrev soobshcheniy?")
    await state.set_state(RequestStates.warmup)

@dp.message(state=RequestStates.warmup)
async def on_warmup(message: Message, state: FSMContext):
    await state.update_data(warmup=message.text)
    await message.answer("Vash kontakt (telefon/email/telegram):")
    await state.set_state(RequestStates.contact)

@dp.message(state=RequestStates.contact)
async def on_contact(message: Message, state: FSMContext):
    await state.update_data(contact=message.text)
    data = await state.get_data()
    role = data.get("role")
    answers = {
        "traffic": data.get("traffic"),
        "lead_magnet": data.get("lead_magnet"),
        "free_offer": data.get("free_offer"),
        "product_sale": data.get("product_sale"),
        "warmup": data.get("warmup"),
        "contact": data.get("contact"),
    }
    user = message.from_user
    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
    record = {"user_id": user.id, "username": user.username or "", "full_name": full_name, "role": role, "answers": json.dumps(answers, ensure_ascii=False)}
    req_id = save_request(record)
    summary = build_admin_summary(req_id, {"full_name": full_name, "username": user.username}, role, answers)
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=summary)
    await message.answer(f"Spasibo! Zayavka #{req_id} prinyata. My svyazhemsya s vami.")
    await state.clear()

@dp.message(state=RequestStates.niche)
async def on_niche(message: Message, state: FSMContext):
    await state.update_data(niche=message.text)
    await message.answer("Dlya chego bot?")
    await state.set_state(RequestStates.bot_purpose)

@dp.message(state=RequestStates.bot_purpose)
async def on_bot_purpose(message: Message, state: FSMContext):
    await state.update_data(bot_purpose=message.text)
    await message.answer("Kakie funktsii?")
    await state.set_state(RequestStates.functions)

@dp.message(state=RequestStates.functions)
async def on_functions(message: Message, state: FSMContext):
    await state.update_data(functions=message.text)
    await message.answer("Byudzhet:")
    await state.set_state(RequestStates.budget)

@dp.message(state=RequestStates.budget)
async def on_budget(message: Message, state: FSMContext):
    await state.update_data(budget=message.text)
    await message.answer("Vash kontakt (telefon/email/telegram):")
    await state.set_state(RequestStates.contact_biz)

@dp.message(state=RequestStates.contact_biz)
async def on_contact_biz(message: Message, state: FSMContext):
    await state.update_data(contact_biz=message.text)
    data = await state.get_data()
    role = data.get("role")
    answers = {"niche": data.get("niche"), "bot_purpose": data.get("bot_purpose"), "functions": data.get("functions"), "budget": data.get("budget"), "contact": data.get("contact_biz")}
    user = message.from_user
    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
    record = {"user_id": user.id, "username": user.username or "", "full_name": full_name, "role": role, "answers": json.dumps(answers, ensure_ascii=False)}
    req_id = save_request(record)
    summary = build_admin_summary(req_id, {"full_name": full_name, "username": user.username}, role, answers)
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=summary)
    await message.answer(f"Spasibo! Zayavka #{req_id} prinyata. My svyazhemsya s vami.")
    await state.clear()

@dp.message(Command(commands=["cancel"]))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Zayavka otmenena. Nachnite zanovo: /start")

async def on_startup(_):
    init_db()

if __name__ == "__main__":
    from aiogram import executor
    print("Bot starting...")
    dp.startup.register(on_startup)
    executor.start_polling(dp, skip_updates=True)
'@

$reqText = "aiogram>=3,<4"

Set-Content -Path "$path\bot.py" -Value $botCode -Encoding UTF8
Set-Content -Path "$path\requirements.txt" -Value $reqText -Encoding UTF8

Write-Host "Bot files created in C:\Telegram"