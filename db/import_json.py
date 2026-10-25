"""Перенос данных проекта из JSON-файлов в базу данных SQLite."""

import json

from db.database import BASE_DIR, get_connection

DATA_DIR = BASE_DIR / "data"
PURCHASES_FILE = DATA_DIR / "purchases.json"
USERS_FILE = DATA_DIR / "users.json"
PARTICIPATIONS_FILE = DATA_DIR / "participations.json"


def load_json(filename: object) -> list:
    """Прочитать список записей из JSON-файла."""
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def import_purchases(conn: object) -> None:
    """Перенести совместные покупки в таблицу purchases."""
    purchases = load_json(PURCHASES_FILE)
    conn.executemany(
        """
        INSERT INTO purchases (
            id,
            product,
            price,
            min_participants,
            max_participants
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (
                item["id"],
                item["product"],
                item["price"],
                item["min_participants"],
                item["max_participants"],
            )
            for item in purchases
        ],
    )


def import_users(conn: object) -> None:
    """Перенести пользователей в таблицу users."""
    users = load_json(USERS_FILE)
    conn.executemany(
        """
        INSERT INTO users (id, name, email)
        VALUES (?, ?, ?)
        """,
        [
            (item["id"], item["name"], item["email"])
            for item in users
        ],
    )


def import_participations(conn: object) -> None:
    """Перенести участия в таблицу participations."""
    participations = load_json(PARTICIPATIONS_FILE)
    conn.executemany(
        """
        INSERT INTO participations (
            id,
            purchase_id,
            user_id,
            is_cancelled
        )
        VALUES (?, ?, ?, ?)
        """,
        [
            (
                item["id"],
                item["purchase_id"],
                item["user_id"],
                int(item["is_cancelled"]),
            )
            for item in participations
        ],
    )


def clear_tables(conn: object) -> None:
    """Очистить таблицы, чтобы импорт можно было выполнить повторно."""
    conn.execute("DELETE FROM participations")
    conn.execute("DELETE FROM users")
    conn.execute("DELETE FROM purchases")


def main() -> None:
    """Выполнить перенос данных из JSON в базу данных."""
    conn = get_connection()
    try:
        clear_tables(conn)
        import_purchases(conn)
        import_users(conn)
        import_participations(conn)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
