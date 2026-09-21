"""Платформа совместных покупок — начальный сценарий (ПР1)."""

from datetime import date

# --- Данные совместной покупки (простые типы) ---
product_name = "Кофе в зёрнах, 1 кг"   # str
product_price = 1200.0                   # float — цена за единицу товара
min_participants = 5                     # int — минимум участников
max_participants = 10                    # int — максимум участников
current_participants = 4                 # int — сейчас участников
commission_percent = 5                   # int — комиссия платформы в процентах
deadline = date(2026, 9, 20)             # дата окончания сбора


def can_join(current: int, maximum: int) -> bool:
    """Проверяет, есть ли свободное место в совместной покупке."""
    return current < maximum


def participant_cost(price: float, commission: int) -> float:
    """Считает стоимость участия для одного покупателя с учётом комиссии."""
    return price + price * commission / 100


def purchase_status(current: int, minimum: int) -> str:
    """Определяет статус покупки: набирается или уже состоялась."""
    if current >= minimum:
        return "Покупка состоялась"
    else:
        remaining = minimum - current
        return f"Идёт набор, не хватает участников: {remaining}"


def payment_status(is_paid: bool) -> str:
    """Возвращает текстовый статус платежа участника."""
    if is_paid:
        return "Платёж подтверждён"
    return "Платёж не внесён"


# --- Сценарий: новый пользователь хочет присоединиться к покупке ---
print(f"Товар: {product_name}")
print(f"Цена за единицу: {product_price} руб.")
print(f"Участников: {current_participants} из {max_participants}")
print(f"Срок сбора до: {deadline}")

if can_join(current_participants, max_participants):
    # пользователь присоединяется — увеличиваем счётчик
    current_participants = current_participants + 1
    cost = participant_cost(product_price, commission_percent)
    # преобразование типов: округляем и приводим к int для вывода
    cost_int = round(cost)
    print("Вы присоединились к совместной покупке!")
    print(
        f"Стоимость вашего участия: {cost_int} руб. "
        f"(с комиссией {commission_percent}%)",
    )
else:
    print("К сожалению, свободных мест нет.")

print(purchase_status(current_participants, min_participants))
print(payment_status(False))
