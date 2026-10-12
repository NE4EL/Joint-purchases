"""Маршруты приложения participations."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.participations, name="participations"),
    path(
        "<int:participation_id>/",
        views.participation_detail,
        name="participation_detail",
    ),
]
