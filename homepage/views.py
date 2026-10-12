"""View-функции главной страницы и общий каркас страниц."""

from django.http import HttpRequest, HttpResponse


def page(title: str, content: str) -> str:
    """Собрать HTML-страницу с общим каркасом и навигацией."""
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{bootstrap}">
</head>
<body>
    <nav class="nav">
        <a class="nav-link" href="/">Главная</a>
        <a class="nav-link" href="/purchases/">Покупки</a>
        <a class="nav-link" href="/participations/">Участия</a>
    </nav>
    <main class="container mt-4">{content}</main>
</body>
</html>"""


def index(request: HttpRequest) -> HttpResponse:
    """Главная страница приложения."""
    content = """
    <h1 class="display-4">Платформа совместных покупок</h1>
    <p class="lead">Совместные покупки товаров оптом.</p>
    <p>Основные разделы:</p>
    <a href="/purchases/" class="btn btn-primary me-2">Покупки</a>
    <a href="/participations/" class="btn btn-secondary">Участия</a>
    """
    return HttpResponse(page("Платформа совместных покупок", content))


def page_not_found(request: HttpRequest, exception) -> HttpResponse:
    """Собственная страница ошибки 404."""
    content = """
    <h1 class="text-danger">404 — страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 — страница не найдена", content),
        status=404,
    )
