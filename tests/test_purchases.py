"""Тесты функций работы с совместными покупками."""

from purchases import (
    add_purchase,
    check_price,
    filter_purchases_by_price,
    find_purchase,
    participant_cost,
    sort_purchases,
)


def test_add_purchase():
    """Новая покупка добавляется в словарь."""
    purchases = {}
    add_purchase(purchases, "Кофе", 1200.0, 5, 10)
    assert len(purchases) == 1


def test_find_purchase():
    """Поиск находит покупку по части названия."""
    purchases = {}
    add_purchase(purchases, "Кофе в зёрнах", 1200.0, 5, 10)
    assert find_purchase(purchases, "кофе")


def test_check_price():
    """Цена покупки не превышает заданный предел."""
    purchases = {}
    purchase_id = add_purchase(purchases, "Чай", 800.0, 3, 6)
    assert check_price(purchases, purchase_id, 1000.0)


def test_filter_purchases_by_price():
    """Отбор возвращает только недорогие покупки."""
    purchases = {}
    add_purchase(purchases, "Чай", 800.0, 3, 6)
    add_purchase(purchases, "Кофе", 1200.0, 5, 10)
    selected = dict(filter_purchases_by_price(purchases, 1000.0))
    assert len(selected) == 1


def test_sort_purchases():
    """Сортировка упорядочивает покупки по возрастанию цены."""
    purchases = {}
    add_purchase(purchases, "Кофе", 1200.0, 5, 10)
    add_purchase(purchases, "Чай", 800.0, 3, 6)
    ordered = sort_purchases(purchases)
    assert ordered[0][1]["price"] == 800.0


def test_participant_cost():
    """Стоимость участия учитывает комиссию платформы."""
    assert participant_cost(1000.0, 5) == 1050.0
