"""Тесты класса Purchase и функций работы с покупками."""

from models import Purchase
from models.purchases import (
    add_purchase,
    filter_purchases_by_price,
    find_purchase,
    sort_purchases,
)


def test_purchase_creation():
    """Атрибуты объекта Purchase сохраняются при создании."""
    purchase = Purchase(1, "Кофе", 1200.0, 5, 10)
    assert purchase.id == 1
    assert purchase.product == "Кофе"
    assert purchase.price == 1200.0


def test_purchase_str():
    """Строковое представление содержит название товара."""
    purchase = Purchase(1, "Кофе", 1200.0, 5, 10)
    assert "Кофе" in str(purchase)


def test_has_free_slots():
    """Метод has_free_slots учитывает максимум участников."""
    purchase = Purchase(1, "Кофе", 1200.0, 5, 10)
    assert purchase.has_free_slots(9)
    assert not purchase.has_free_slots(10)


def test_participant_cost():
    """Метод participant_cost учитывает комиссию платформы."""
    purchase = Purchase(1, "Кофе", 1000.0, 5, 10)
    assert purchase.participant_cost(5) == 1050.0


def test_add_purchase():
    """Новая покупка добавляется в коллекцию объектов."""
    purchases = []
    add_purchase(purchases, "Кофе", 1200.0, 5, 10)
    assert len(purchases) == 1
    assert isinstance(purchases[0], Purchase)


def test_find_purchase():
    """Поиск находит покупку по части названия."""
    purchases = []
    add_purchase(purchases, "Кофе в зёрнах", 1200.0, 5, 10)
    assert find_purchase(purchases, "кофе")


def test_filter_purchases_by_price():
    """Отбор возвращает только недорогие покупки."""
    purchases = []
    add_purchase(purchases, "Чай", 800.0, 3, 6)
    add_purchase(purchases, "Кофе", 1200.0, 5, 10)
    selected = list(filter_purchases_by_price(purchases, 1000.0))
    assert len(selected) == 1


def test_sort_purchases():
    """Сортировка упорядочивает покупки по возрастанию цены."""
    purchases = []
    add_purchase(purchases, "Кофе", 1200.0, 5, 10)
    add_purchase(purchases, "Чай", 800.0, 3, 6)
    ordered = sort_purchases(purchases)
    assert ordered[0].price == 800.0
