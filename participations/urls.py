"""Маршруты приложения participations."""

from django.urls import path

from . import views

app_name = "participations"

urlpatterns = [
    path("", views.participations, name="list"),
    path("statistics/", views.statistics, name="statistics"),
    path(
        "<int:participation_id>/",
        views.participation_detail,
        name="detail",
    ),
]
