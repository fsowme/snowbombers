from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="bot_index"),
    path("webhook/", views.webhook_updater, name="webhook"),
]
