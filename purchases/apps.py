"""Конфигурация приложения purchases."""

from django.apps import AppConfig


class PurchasesConfig(AppConfig):
    """Настройки приложения purchases."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "purchases"
