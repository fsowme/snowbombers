from django.core.paginator import Paginator
from ski.models import Continent, Country, Resort
from telegram import InlineKeyboardButton


def continents_buttons():
    paginator = Paginator(Continent.objects.all().order_by("name"), 2)
    keyboard = []
    for page in paginator:
        keyboard.append(
            [
                InlineKeyboardButton(
                    _.name,
                    callback_data=f"continent:{_.name}",
                )
                for _ in page
            ]
        )
    return keyboard


def countries_buttons(continent_name):
    continent = Continent.objects.get(name=continent_name)
    paginator = Paginator(
        Country.objects.filter(continent=continent).order_by("name"), 3
    )
    keyboard = []
    for page in paginator:
        keyboard.append(
            [
                InlineKeyboardButton(_.name, callback_data=f"country:{_.name}")
                for _ in page
            ]
        )
    keyboard.append(
        [
            InlineKeyboardButton(
                "Back to list of continents", callback_data="start_info:"
            )
        ]
    )
    return keyboard


def resorts_buttons(country_name):
    continent = Continent.objects.get(countries__name=country_name).name
    paginator = Paginator(
        Resort.objects.filter(country__name=country_name).order_by("name"), 3
    )
    keyboard = []
    for page in paginator:
        keyboard.append(
            [
                InlineKeyboardButton(_.name, callback_data=f"resort:{_.name}")
                for _ in page
            ]
        )
    keyboard.append(
        [
            InlineKeyboardButton(
                "Back to list of countries",
                callback_data=f"continent:{continent}",
            )
        ]
    )
    return keyboard
