"""Класс Participation и функции работы с участием в покупках."""

from .purchases import Purchase
from .users import User


class Participation:
    """Участие пользователя в совместной покупке."""

    def __init__(
        self,
        participation_id: int,
        purchase: Purchase,
        user: User,
    ) -> None:
        """Создать объект участия."""
        self.id = participation_id
        self.purchase = purchase
        self.user = user
        self.is_cancelled = False

    def cancel(self) -> None:
        """Отменить участие (изменить состояние, не удаляя объект)."""
        self.is_cancelled = True

    def __str__(self) -> str:
        """Вернуть строковое представление участия."""
        state = "отменено" if self.is_cancelled else "активно"
        return (
            f"{self.id}. {self.user.name} — "
            f"{self.purchase.product} ({state})"
        )


def count_active(
    participations: list[Participation],
    purchase: Purchase,
) -> int:
    """Посчитать число активных участников покупки."""
    total = 0
    for item in participations:
        if item.purchase.id == purchase.id and not item.is_cancelled:
            total += 1
    return total


def is_available(
    participations: list[Participation],
    purchase: Purchase,
) -> bool:
    """Проверить, есть ли в покупке свободные места."""
    return purchase.has_free_slots(count_active(participations, purchase))


def join_purchase(
    participations: list[Participation],
    purchase: Purchase,
    user: User,
) -> Participation | None:
    """Создать участие, если в покупке есть места, иначе вернуть None."""
    if not is_available(participations, purchase):
        return None
    new_id = max((item.id for item in participations), default=0) + 1
    participation = Participation(new_id, purchase, user)
    participations.append(participation)
    return participation


def cancel_participation(
    participations: list[Participation],
    participation_id: int,
) -> bool:
    """Отменить участие по идентификатору (вызвать его метод cancel)."""
    for item in participations:
        if item.id == participation_id:
            item.cancel()
            return True
    return False


def purchase_status(
    participations: list[Participation],
    purchase: Purchase,
) -> str:
    """Вернуть текстовый статус покупки (функция из ПР1/ПР2)."""
    current = count_active(participations, purchase)
    if purchase.is_reached(current):
        return "Покупка состоялась"
    remaining = purchase.min_participants - current
    return f"Идёт набор, не хватает участников: {remaining}"
