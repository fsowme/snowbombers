from django.core.paginator import Paginator
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from ski.models import Continent, Country, Resort

from .models import User as django_user


def continents_buttons():
    paginator = Paginator(Continent.objects.all().order_by("name"), 2)
    keyboard = []
    for page in paginator:
        keyboard.append(
            [
                InlineKeyboardButton(
                    _.name,
                    callback_data=f"info_continent:{_.name}",
                )
                for _ in page
            ]
        )
    keyboard.append([InlineKeyboardButton("Quit", callback_data="cancel")])
    return InlineKeyboardMarkup(keyboard)


def countries_buttons(continent_name):
    continent = Continent.objects.get(name=continent_name)
    paginator = Paginator(
        Country.objects.filter(continent=continent).order_by("name"), 3
    )
    keyboard = []
    for page in paginator:
        keyboard.append(
            [
                InlineKeyboardButton(
                    _.name, callback_data=f"info_country:{_.name}"
                )
                for _ in page
            ]
        )
    keyboard.append(
        [
            InlineKeyboardButton(
                "Back to list of continents", callback_data="info_start:"
            ),
            InlineKeyboardButton("Quit", callback_data="cancel"),
        ]
    )
    return InlineKeyboardMarkup(keyboard)


def resorts_buttons(country_name):
    continent_name = Continent.objects.get(countries__name=country_name).name
    paginator = Paginator(
        Resort.objects.filter(country__name=country_name).order_by("name"), 3
    )
    keyboard = []
    for page in paginator:
        keyboard.append(
            [
                InlineKeyboardButton(
                    _.name, callback_data=f"info_resort:{_.uuid}"
                )
                for _ in page
            ]
        )
    keyboard.append(
        [
            InlineKeyboardButton(
                "Back to list of countries",
                callback_data=f"info_continent:{continent_name}",
            ),
            InlineKeyboardButton("Quit", callback_data="cancel"),
        ]
    )
    return InlineKeyboardMarkup(keyboard)


def get_resort_info(uuid):
    resort = Resort.objects.get(uuid=uuid)
    top_point = resort.top_point
    height_difference = resort.height_difference()
    blue = resort.slopes.blue_slopes
    red = resort.slopes.red_slopes
    black = resort.slopes.black_slopes
    all_slopes = resort.slopes.all_slopes
    resort_info = (
        f"{resort.name}\nRed: {red}, Blue: {blue}, Black: {black}, "
        f"All: {all_slopes}\nTop: {top_point} m, "
        f"Height difference: {height_difference} m"
    )
    return resort_info


def add_bookmarks_button(resort_name, user_id=None):
    user = django_user.objects.get(telegram_id=user_id)
    if user.bookmarks.filter(uuid=resort_name).exists():
        button_text = "Remove from bookmarks"
        callback_data = f"bookmarks_del:{resort_name}"
    else:
        button_text = "Add to bookmarks"
        callback_data = f"bookmarks_add:{resort_name}"
    keyboard = [
        [
            InlineKeyboardButton(
                button_text,
                callback_data=callback_data,
            )
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def resort_to_bookmarks(user_id, resort_name):
    print("add")
    user = django_user.objects.get(telegram_id=user_id)
    resort = Resort.objects.get(uuid=resort_name)
    return user.bookmarks.add(resort)


def del_resort_from_bookmarks(user_id, resort_name):
    print("del")
    user = django_user.objects.get(telegram_id=user_id)
    resort = Resort.objects.get(uuid=resort_name)
    return user.bookmarks.remove(resort)


def check_user_start(user_data):
    _, created = django_user.objects.get_or_create(
        telegram_id=user_data.id,
        defaults={
            "first_name": user_data.first_name,
            "is_bot": user_data.is_bot,
        },
    )
    return created


def resorts_in_bookmarks(user_id):
    user = django_user.objects.get(telegram_id=user_id)
    paginator = Paginator(user.bookmarks.all(), 3)
    keyboard = []
    for page in paginator:
        keyboard.append(
            [
                InlineKeyboardButton(
                    _.name, callback_data=f"info_resort:{_.uuid}"
                )
                for _ in page
            ]
        )
    keyboard.append(
        [
            InlineKeyboardButton("Quit", callback_data="cancel"),
        ]
    )
    return InlineKeyboardMarkup(keyboard)
