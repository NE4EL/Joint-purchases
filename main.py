"""Платформа совместных покупок — точка входа приложения (ПР3)."""

from models import Participation, Purchase, User
from models.participations import (
    cancel_participation,
    count_active,
    join_purchase,
    purchase_status,
)
from models.purchases import (
    filter_purchases_by_price,
    find_purchase,
    find_purchase_by_id,
    sort_purchases,
)
from models.users import find_user_by_id
from storage import (
    load_participations,
    load_purchases,
    load_users,
    save_participations,
)
from utils import input_int, input_str

PURCHASES_FILE = "data/purchases.json"
USERS_FILE = "data/users.json"
PARTICIPATIONS_FILE = "data/participations.json"

MENU = (
    "\n=== Платформа совместных покупок ===\n"
    "1. Показать совместные покупки\n"
    "2. Найти покупку по названию\n"
    "3. Отобрать покупки не дороже суммы\n"
    "4. Показать покупки по возрастанию цены\n"
    "5. Показать пользователей\n"
    "6. Присоединиться к покупке\n"
    "7. Отменить участие\n"
    "8. Показать участия\n"
    "0. Выход"
)


def show_purchases(
    purchases: list[Purchase],
    participations: list[Participation],
) -> None:
    """Вывести список совместных покупок со статусом набора."""
    if not purchases:
        print("Список совместных покупок пуст.")
        return
    for purchase in purchases:
        current = count_active(participations, purchase)
        status = purchase_status(participations, purchase)
        print(
            f"{purchase} участников "
            f"{current}/{purchase.max_participants} ({status})",
        )


def show_users(users: list[User]) -> None:
    """Вывести список пользователей."""
    if not users:
        print("Список пользователей пуст.")
        return
    for user in users:
        print(user)


def show_participations(participations: list[Participation]) -> None:
    """Вывести список участий."""
    if not participations:
        print("Пока нет ни одного участия.")
        return
    for item in participations:
        print(item)


def create_new_participation(
    purchases: list[Purchase],
    users: list[User],
    participations: list[Participation],
) -> None:
    """Создать участие: выбрать покупку и пользователя, проверить места."""
    purchase = find_purchase_by_id(purchases, input_int("Номер покупки: "))
    if purchase is None:
        print("Покупка с таким номером не найдена.")
        return
    user = find_user_by_id(users, input_int("Ваш номер пользователя: "))
    if user is None:
        print("Пользователь с таким номером не найден.")
        return
    participation = join_purchase(participations, purchase, user)
    if participation is None:
        print("Свободных мест в покупке больше нет.")
        return
    print(f"Участие создано: {participation}")


def cancel_action(participations: list[Participation]) -> None:
    """Отменить участие по его номеру."""
    participation_id = input_int("Номер участия для отмены: ")
    if cancel_participation(participations, participation_id):
        print("Участие отменено.")
    else:
        print("Участие с таким номером не найдено.")


def process(
    choice: int,
    purchases: list[Purchase],
    users: list[User],
    participations: list[Participation],
) -> None:
    """Выполнить выбранное пользователем действие меню."""
    if choice == 1:
        show_purchases(purchases, participations)
    elif choice == 2:
        query = input_str("Введите часть названия: ")
        show_purchases(find_purchase(purchases, query), participations)
    elif choice == 3:
        max_price = input_int("Максимальная цена, руб.: ")
        selected = list(filter_purchases_by_price(purchases, max_price))
        show_purchases(selected, participations)
    elif choice == 4:
        show_purchases(sort_purchases(purchases), participations)
    elif choice == 5:
        show_users(users)
    elif choice == 6:
        create_new_participation(purchases, users, participations)
    elif choice == 7:
        cancel_action(participations)
    elif choice == 8:
        show_participations(participations)
    else:
        print("Неизвестный пункт меню.")


def main() -> None:
    """Запустить главное меню приложения."""
    purchases = load_purchases(PURCHASES_FILE)
    users = load_users(USERS_FILE)
    participations = load_participations(
        PARTICIPATIONS_FILE,
        purchases,
        users,
    )
    while True:
        print(MENU)
        choice = input_int("Выберите действие: ")
        if choice == 0:
            print("Выход из программы.")
            break
        process(choice, purchases, users, participations)
        save_participations(PARTICIPATIONS_FILE, participations)


if __name__ == "__main__":
    main()
