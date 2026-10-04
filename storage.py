"""Загрузка и сохранение данных проекта в JSON-файлах."""

import json

from models import Participation, Purchase, User
from models.purchases import find_purchase_by_id
from models.users import find_user_by_id


def _read_json(filename: str) -> list:
    """Прочитать список из JSON-файла, вернуть [] при ошибке."""
    try:
        with open(filename, encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def _write_json(filename: str, data: list) -> None:
    """Записать список в JSON-файл."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_purchases(filename: str) -> list[Purchase]:
    """Загрузить совместные покупки из JSON-файла в объекты Purchase."""
    purchases = []
    for item in _read_json(filename):
        purchase = Purchase(
            item["id"],
            item["product"],
            item["price"],
            item["min_participants"],
            item["max_participants"],
        )
        purchases.append(purchase)
    return purchases


def save_purchases(filename: str, purchases: list[Purchase]) -> None:
    """Сохранить объекты Purchase в JSON-файл."""
    data = [
        {
            "id": p.id,
            "product": p.product,
            "price": p.price,
            "min_participants": p.min_participants,
            "max_participants": p.max_participants,
        }
        for p in purchases
    ]
    _write_json(filename, data)


def load_users(filename: str) -> list[User]:
    """Загрузить пользователей из JSON-файла в объекты User."""
    return [User.from_data(item) for item in _read_json(filename)]


def save_users(filename: str, users: list[User]) -> None:
    """Сохранить объекты User в JSON-файл."""
    data = [
        {"id": u.id, "name": u.name, "email": u.email}
        for u in users
    ]
    _write_json(filename, data)


def load_participations(
    filename: str,
    purchases: list[Purchase],
    users: list[User],
) -> list[Participation]:
    """Загрузить участия из JSON, восстановив связи с Purchase и User."""
    participations = []
    for item in _read_json(filename):
        purchase = find_purchase_by_id(purchases, item["purchase_id"])
        user = find_user_by_id(users, item["user_id"])
        if purchase is None or user is None:
            continue
        participation = Participation(item["id"], purchase, user)
        participation.is_cancelled = item["is_cancelled"]
        participations.append(participation)
    return participations


def save_participations(
    filename: str,
    participations: list[Participation],
) -> None:
    """Сохранить объекты Participation в JSON (ссылки → идентификаторы)."""
    data = [
        {
            "id": item.id,
            "purchase_id": item.purchase.id,
            "user_id": item.user.id,
            "is_cancelled": item.is_cancelled,
        }
        for item in participations
    ]
    _write_json(filename, data)
