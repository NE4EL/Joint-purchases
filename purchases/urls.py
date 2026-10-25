"""Маршруты приложения purchases."""

from django.urls import path

from . import views

app_name = "purchases"

urlpatterns = [
    path("", views.purchases, name="list"),
    path("search/", views.search, name="search"),
    path("<int:purchase_id>/", views.purchase_detail, name="detail"),
]
