import sqlite3
import json
from datetime import datetime
from config import DB_PATH


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            username TEXT,
            full_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_telegram_id INTEGER,
            who_text TEXT,
            what_wants TEXT,
            platform TEXT,
            functions TEXT,
            budget TEXT,
            when_launch TEXT,
            contact TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_telegram_id) REFERENCES users (telegram_id)
        )
    """)
    
    conn.commit()
    conn.close()


def add_user(telegram_id: int, username: str, full_name: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT OR IGNORE INTO users (telegram_id, username, full_name)
        VALUES (?, ?, ?)
    """, (telegram_id, username, full_name))
    conn.commit()
    conn.close()


def get_user(telegram_id: int):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
    user = cur.fetchone()
    conn.close()
    return user


def get_user_count() -> int:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users")
    count = cur.fetchone()[0]
    conn.close()
    return count


def save_application(data: dict) -> int:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO applications (
            user_telegram_id, who_text, what_wants, platform,
            functions, budget, when_launch, contact
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["telegram_id"],
        data["who_text"],
        data["what_wants"],
        data["platform"],
        data["functions"],
        data["budget"],
        data["when_launch"],
        data["contact"]
    ))
    last_id = cur.lastrowid
    conn.commit()
    conn.close()
    return last_id


def get_application_count() -> int:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM applications")
    count = cur.fetchone()[0]
    conn.close()
    return count


def get_today_application_count() -> int:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) FROM applications 
        WHERE DATE(created_at) = DATE('now')
    """)
    count = cur.fetchone()[0]
    conn.close()
    return count