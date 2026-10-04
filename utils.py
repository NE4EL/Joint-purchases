"""Вспомогательные функции безопасного ввода."""


def input_int(prompt: str) -> int:
    """Запросить целое число, повторяя запрос при ошибке ввода."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Введите целое число.")


def input_str(prompt: str) -> str:
    """Запросить непустую строку, повторяя запрос при ошибке ввода."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Значение не должно быть пустым.")
