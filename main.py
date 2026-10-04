"""Платформа совместных покупок — точка входа приложения (ПР2)."""

from participations import (
    cancel_participation,
    count_participants,
    join_purchase,
    purchase_status,
)
from purchases import (
    filter_purchases_by_price,
    find_purchase,
    sort_purchases,
)
from storage import (
    load_participations,
    load_purchases,
    save_participations,
)
from utils import input_int, input_str

PURCHASES_FILE = "data/purchases.json"
PARTICIPATIONS_FILE = "data/participations.json"

MENU = (
    "\n=== Платформа совместных покупок ===\n"
    "1. Показать совместные покупки\n"
    "2. Найти покупку по названию\n"
    "3. Отобрать покупки не дороже суммы\n"
    "4. Показать покупки по возрастанию цены\n"
    "5. Присоединиться к покупке\n"
    "6. Отменить участие\n"
    "7. Показать участия\n"
    "0. Выход"
)


def show_purchases(
    purchases: dict[int, dict],
    participations: list[dict],
) -> None:
    """Вывести список совместных покупок с числом участников."""
    if not purchases:
        print("Список совместных покупок пуст.")
        return
    for purchase_id, data in purchases.items():
        current = count_participants(participations, purchase_id)
        status = purchase_status(current, data["min_participants"])
        print(
            f"{purchase_id}. {data['product']} — "
            f"{data['price']} руб., участников "
            f"{current}/{data['max_participants']} ({status})",
        )


def show_participations(
    participations: list[dict],
    purchases: dict[int, dict],
) -> None:
    """Вывести список участий в покупках."""
    if not participations:
        print("Пока нет ни одного участия.")
        return
    for item in participations:
        purchase = purchases.get(item["purchase_id"])
        product = purchase["product"] if purchase else "неизвестный товар"
        print(f"{item['id']}. {item['user']} — {product}")


def join_action(
    purchases: dict[int, dict],
    participations: list[dict],
) -> None:
    """Присоединить участника к выбранной покупке."""
    purchase_id = input_int("Номер покупки: ")
    if purchase_id not in purchases:
        print("Покупка с таким номером не найдена.")
        return
    user = input_str("Ваше имя: ")
    max_participants = purchases[purchase_id]["max_participants"]
    try:
        join_purchase(participations, purchase_id, user, max_participants)
    except ValueError as error:
        print(error)
        return
    print("Вы успешно присоединились к покупке.")


def cancel_action(participations: list[dict]) -> None:
    """Отменить участие по его номеру."""
    participation_id = input_int("Номер участия для отмены: ")
    if cancel_participation(participations, participation_id):
        print("Участие отменено.")
    else:
        print("Участие с таким номером не найдено.")


def process(
    choice: int,
    purchases: dict[int, dict],
    participations: list[dict],
) -> None:
    """Выполнить выбранное пользователем действие меню."""
    if choice == 1:
        show_purchases(purchases, participations)
    elif choice == 2:
        query = input_str("Введите часть названия: ")
        show_purchases(find_purchase(purchases, query), participations)
    elif choice == 3:
        max_price = input_int("Максимальная цена, руб.: ")
        selected = dict(filter_purchases_by_price(purchases, max_price))
        show_purchases(selected, participations)
    elif choice == 4:
        show_purchases(dict(sort_purchases(purchases)), participations)
    elif choice == 5:
        join_action(purchases, participations)
    elif choice == 6:
        cancel_action(participations)
    elif choice == 7:
        show_participations(participations, purchases)
    else:
        print("Неизвестный пункт меню.")


def main() -> None:
    """Запустить главное меню приложения."""
    purchases = load_purchases(PURCHASES_FILE)
    participations = load_participations(PARTICIPATIONS_FILE)
    while True:
        print(MENU)
        choice = input_int("Выберите действие: ")
        if choice == 0:
            print("Выход из программы.")
            break
        process(choice, purchases, participations)
        save_participations(PARTICIPATIONS_FILE, participations)


if __name__ == "__main__":
    main()
