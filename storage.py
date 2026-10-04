"""Загрузка и сохранение данных проекта в JSON-файлах."""

import json


def load_purchases(filename: str) -> dict[int, dict]:
    """Загрузить совместные покупки из JSON-файла."""
    try:
        with open(filename, encoding="utf-8") as file:
            items = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    purchases = {}
    for item in items:
        purchases[item["id"]] = {
            "product": item["product"],
            "price": item["price"],
            "min_participants": item["min_participants"],
            "max_participants": item["max_participants"],
        }
    return purchases


def save_purchases(filename: str, purchases: dict[int, dict]) -> None:
    """Сохранить совместные покупки в JSON-файл."""
    items = [{"id": purchase_id, **data}
             for purchase_id, data in purchases.items()]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(items, file, ensure_ascii=False, indent=4)


def load_participations(filename: str) -> list[dict]:
    """Загрузить участия из JSON-файла."""
    try:
        with open(filename, encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_participations(filename: str, participations: list[dict]) -> None:
    """Сохранить участия в JSON-файл."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(participations, file, ensure_ascii=False, indent=4)
