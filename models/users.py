"""Класс User и функции работы с пользователями."""


class User:
    """Пользователь платформы совместных покупок."""

    def __init__(self, user_id: int, name: str, email: str) -> None:
        """Создать объект пользователя."""
        self.id = user_id
        self.name = name
        self.email = email

    @classmethod
    def from_data(cls, data: dict) -> "User":
        """Создать объект пользователя из набора данных (JSON)."""
        return cls(data["id"], data["name"], data["email"])

    def __str__(self) -> str:
        """Вернуть строковое представление пользователя."""
        return f"{self.id}. {self.name} ({self.email})"


def add_user(users: list[User], name: str, email: str) -> User:
    """Создать пользователя, добавить его в коллекцию и вернуть объект."""
    new_id = max((u.id for u in users), default=0) + 1
    user = User(new_id, name, email)
    users.append(user)
    return user


def find_user(users: list[User], query: str) -> list[User]:
    """Найти пользователей по имени или адресу электронной почты."""
    text = query.lower()
    return [
        u for u in users
        if text in u.name.lower() or text in u.email.lower()
    ]


def find_user_by_id(users: list[User], user_id: int) -> User | None:
    """Найти пользователя по идентификатору."""
    for user in users:
        if user.id == user_id:
            return user
    return None
