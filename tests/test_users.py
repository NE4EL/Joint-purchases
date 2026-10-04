"""Тесты класса User и функций работы с пользователями."""

from models import User
from models.users import add_user, find_user


def test_user_creation():
    """Атрибуты объекта User сохраняются при создании."""
    user = User(1, "Иван Петров", "ivan@example.com")
    assert user.id == 1
    assert user.name == "Иван Петров"
    assert user.email == "ivan@example.com"


def test_user_from_data():
    """Метод from_data создаёт пользователя из словаря."""
    data = {"id": 2, "name": "Анна", "email": "anna@example.com"}
    user = User.from_data(data)
    assert isinstance(user, User)
    assert user.id == 2


def test_user_str():
    """Строковое представление содержит имя пользователя."""
    user = User(1, "Иван Петров", "ivan@example.com")
    assert "Иван Петров" in str(user)


def test_add_user():
    """Новый пользователь добавляется в коллекцию объектов."""
    users = []
    add_user(users, "Иван", "ivan@example.com")
    assert len(users) == 1
    assert isinstance(users[0], User)


def test_find_user():
    """Поиск находит пользователя по имени или почте."""
    users = []
    add_user(users, "Иван Петров", "ivan@example.com")
    assert find_user(users, "иван")
    assert find_user(users, "example.com")
