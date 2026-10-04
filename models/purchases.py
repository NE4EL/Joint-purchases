"""Класс Purchase и функции работы с совместными покупками."""

from collections.abc import Iterator


class Purchase:
    """Совместная покупка товара."""

    def __init__(
        self,
        purchase_id: int,
        product: str,
        price: float,
        min_participants: int,
        max_participants: int,
    ) -> None:
        """Создать объект совместной покупки."""
        self.id = purchase_id
        self.product = product
        self.price = price
        self.min_participants = min_participants
        self.max_participants = max_participants

    def has_free_slots(self, current: int) -> bool:
        """Проверить, есть ли свободные места при текущем числе участников."""
        return current < self.max_participants

    def is_reached(self, current: int) -> bool:
        """Проверить, набрано ли минимальное число участников."""
        return current >= self.min_participants

    def participant_cost(self, commission_percent: int) -> float:
        """Рассчитать стоимость участия с учётом комиссии платформы."""
        return self.price + self.price * commission_percent / 100

    @staticmethod
    def validate_price(price: float) -> bool:
        """Проверить корректность цены (метод класса, без self)."""
        return price > 0

    def __str__(self) -> str:
        """Вернуть строковое представление покупки."""
        return f"{self.id}. {self.product} — {self.price} руб."


def add_purchase(
    purchases: list[Purchase],
    product: str,
    price: float,
    min_participants: int,
    max_participants: int,
) -> Purchase:
    """Создать покупку, добавить её в коллекцию и вернуть объект."""
    new_id = max((p.id for p in purchases), default=0) + 1
    purchase = Purchase(
        new_id,
        product,
        price,
        min_participants,
        max_participants,
    )
    purchases.append(purchase)
    return purchase


def find_purchase(purchases: list[Purchase], query: str) -> list[Purchase]:
    """Найти покупки по подстроке названия товара."""
    text = query.lower()
    return [p for p in purchases if text in p.product.lower()]


def find_purchase_by_id(
    purchases: list[Purchase],
    purchase_id: int,
) -> Purchase | None:
    """Найти покупку по идентификатору."""
    for purchase in purchases:
        if purchase.id == purchase_id:
            return purchase
    return None


def filter_purchases_by_price(
    purchases: list[Purchase],
    max_price: float,
) -> Iterator[Purchase]:
    """Отобрать покупки с ценой не выше max_price (генератор)."""
    for purchase in purchases:
        if purchase.price <= max_price:
            yield purchase


def sort_purchases(purchases: list[Purchase]) -> list[Purchase]:
    """Вернуть покупки, отсортированные по возрастанию цены."""
    return sorted(purchases, key=lambda purchase: purchase.price)
