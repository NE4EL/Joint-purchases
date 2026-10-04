"""Тесты класса Participation и функций работы с участием."""

from models import Participation, Purchase, User
from models.participations import (
    cancel_participation,
    is_available,
    join_purchase,
    purchase_status,
)


def make_purchase(max_participants: int = 10) -> Purchase:
    """Создать тестовую покупку."""
    return Purchase(1, "Кофе", 1200.0, 2, max_participants)


def make_user() -> User:
    """Создать тестового пользователя."""
    return User(1, "Иван Петров", "ivan@example.com")


def test_participation_creation():
    """Участие хранит ссылки на объекты Purchase и User."""
    purchase = make_purchase()
    user = make_user()
    participation = Participation(1, purchase, user)
    assert participation.purchase is purchase
    assert participation.user is user
    assert not participation.is_cancelled


def test_participation_cancel():
    """Метод cancel изменяет состояние участия."""
    participation = Participation(1, make_purchase(), make_user())
    participation.cancel()
    assert participation.is_cancelled


def test_is_available_empty():
    """В новой покупке есть свободные места."""
    assert is_available([], make_purchase())


def test_join_purchase():
    """Участие создаётся и добавляется в коллекцию."""
    participations = []
    result = join_purchase(participations, make_purchase(), make_user())
    assert isinstance(result, Participation)
    assert len(participations) == 1


def test_join_purchase_full():
    """При отсутствии мест участие не создаётся (возвращается None)."""
    purchase = make_purchase(max_participants=1)
    participations = []
    join_purchase(participations, purchase, make_user())
    assert join_purchase(participations, purchase, make_user()) is None


def test_cancel_frees_slot():
    """Отменённое участие освобождает место в покупке."""
    purchase = make_purchase(max_participants=1)
    participations = []
    first = join_purchase(participations, purchase, make_user())
    cancel_participation(participations, first.id)
    assert is_available(participations, purchase)


def test_purchase_status():
    """Статус покупки меняется при наборе участников."""
    purchase = make_purchase(max_participants=5)
    participations = []
    assert "Идёт набор" in purchase_status(participations, purchase)
    join_purchase(participations, purchase, User(1, "A", "a@e.com"))
    join_purchase(participations, purchase, User(2, "B", "b@e.com"))
    assert purchase_status(participations, purchase) == "Покупка состоялась"
