"""Тесты функций работы с участием в покупках."""

import pytest

from participations import (
    can_join,
    cancel_participation,
    count_participants,
    join_purchase,
    payment_status,
)


def test_can_join_empty():
    """В пустой покупке есть свободные места."""
    assert can_join([], 1, 10)


def test_join_purchase():
    """Участник добавляется в список участий."""
    participations = []
    join_purchase(participations, 1, "Анна", 10)
    assert count_participants(participations, 1) == 1


def test_join_purchase_full():
    """Присоединение к заполненной покупке вызывает ошибку."""
    participations = []
    join_purchase(participations, 1, "Анна", 1)
    with pytest.raises(ValueError):
        join_purchase(participations, 1, "Борис", 1)


def test_cancel_participation():
    """Участие удаляется по идентификатору."""
    participations = []
    new_id = join_purchase(participations, 1, "Анна", 10)
    assert cancel_participation(participations, new_id)


def test_payment_status():
    """Статус платежа зависит от флага оплаты."""
    assert payment_status(True) == "Платёж подтверждён"
