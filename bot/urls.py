from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="bot_index"),
    path("webhook/", views.webhook_updater, name="webhook"),
    path("continents/", views.parse_continents, name="continents"),
    path("countries/", views.parse_countries, name="countries"),
    path("resorts/", views.parse_resorts, name="resorts"),
]
