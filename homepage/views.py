"""View-функции главной страницы и страницы ошибки 404."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(request: HttpRequest) -> HttpResponse:
    """Главная страница приложения."""
    return render(request, "homepage/index.html")


def page_not_found(request: HttpRequest, exception) -> HttpResponse:
    """Собственная страница ошибки 404."""
    return render(request, "404.html", status=404)
