"""Подключение Python к базе данных SQLite проекта."""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = str(BASE_DIR / "data" / "joint_purchases.sqlite")


def get_connection() -> sqlite3.Connection:
    """Создать соединение с базой и включить проверку внешних ключей."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
