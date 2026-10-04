"""Функции работы с участием в совместных покупках."""


def count_participants(
    participations: list[dict],
    purchase_id: int,
) -> int:
    """Посчитать число участников конкретной покупки."""
    total = 0
    for item in participations:
        if item["purchase_id"] == purchase_id:
            total += 1
    return total


def can_join(
    participations: list[dict],
    purchase_id: int,
    max_participants: int,
) -> bool:
    """Проверить, есть ли свободное место в покупке."""
    return count_participants(participations, purchase_id) < max_participants


def join_purchase(
    participations: list[dict],
    purchase_id: int,
    user: str,
    max_participants: int,
) -> int:
    """Присоединить участника к покупке и вернуть идентификатор участия."""
    if not can_join(participations, purchase_id, max_participants):
        raise ValueError("Свободных мест в покупке больше нет.")
    new_id = max(
        (item["id"] for item in participations),
        default=0,
    ) + 1
    participation = {
        "id": new_id,
        "purchase_id": purchase_id,
        "user": user,
    }
    participations.append(participation)
    return new_id


def cancel_participation(
    participations: list[dict],
    participation_id: int,
) -> bool:
    """Отменить участие по идентификатору."""
    for index, item in enumerate(participations):
        if item["id"] == participation_id:
            participations.pop(index)
            return True
    return False


def purchase_status(current: int, minimum: int) -> str:
    """Вернуть текстовый статус покупки (функция из ПР1)."""
    if current >= minimum:
        return "Покупка состоялась"
    return f"Идёт набор, не хватает участников: {minimum - current}"


def payment_status(is_paid: bool) -> str:
    """Вернуть текстовый статус платежа участника (функция из ПР1)."""
    if is_paid:
        return "Платёж подтверждён"
    return "Платёж не внесён"
