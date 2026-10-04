"""Функции работы с совместными покупками."""

from collections.abc import Iterator


def add_purchase(
    purchases: dict[int, dict],
    product: str,
    price: float,
    min_participants: int,
    max_participants: int,
) -> int:
    """Добавить совместную покупку и вернуть её идентификатор."""
    new_id = max(purchases) + 1 if purchases else 1
    purchases[new_id] = {
        "product": product,
        "price": price,
        "min_participants": min_participants,
        "max_participants": max_participants,
    }
    return new_id


def find_purchase(purchases: dict[int, dict], query: str) -> dict[int, dict]:
    """Найти покупки, в названии товара которых есть подстрока query."""
    result = {}
    for purchase_id, data in purchases.items():
        if query.lower() in data["product"].lower():
            result[purchase_id] = data
    return result


def check_price(
    purchases: dict[int, dict],
    purchase_id: int,
    max_price: float,
) -> bool:
    """Проверить, что цена покупки не превышает max_price."""
    return purchases[purchase_id]["price"] <= max_price


def filter_purchases_by_price(
    purchases: dict[int, dict],
    max_price: float,
) -> Iterator[tuple[int, dict]]:
    """Отобрать покупки с ценой не выше max_price (генератор)."""
    for purchase_id, data in purchases.items():
        if data["price"] <= max_price:
            yield purchase_id, data


def sort_purchases(purchases: dict[int, dict]) -> list[tuple[int, dict]]:
    """Вернуть покупки, отсортированные по возрастанию цены."""
    return sorted(
        purchases.items(),
        key=lambda item: item[1]["price"],
    )


def participant_cost(price: float, commission_percent: int) -> float:
    """Рассчитать стоимость участия с учётом комиссии платформы."""
    return price + price * commission_percent / 100
