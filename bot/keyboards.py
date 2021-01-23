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
                    callback_data=_.name,
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
            [InlineKeyboardButton(_.name, callback_data=_.name) for _ in page]
        )
    return keyboard


def resorts_buttons(country_name):
    paginator = Paginator(
        Resort.objects.filter(country__name=country_name).order_by("name"), 3
    )
    keyboard = []
    for page in paginator:
        keyboard.append(
            [InlineKeyboardButton(_.name, callback_data=_.name) for _ in page]
        )
    return keyboard
