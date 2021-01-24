from django.core.paginator import Paginator
from ski.models import Continent, Country, Resort
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


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
                InlineKeyboardButton(_.name, callback_data=f"country:{_.name}")
                for _ in page
            ]
        )
    keyboard.append(
        [
            InlineKeyboardButton(
                "Back to list of continents", callback_data="start_info:"
            ),
            InlineKeyboardButton("Quit", callback_data="cancel"),
        ]
    )
    return InlineKeyboardMarkup(keyboard)


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
            ),
            InlineKeyboardButton("Quit", callback_data="cancel"),
        ]
    )
    return InlineKeyboardMarkup(keyboard)


def get_resort_info(resort_name):
    resort = Resort.objects.get(name=resort_name)
    top_point = resort.top_point
    height_difference = resort.height_difference()
    blue = resort.slopes.blue_slopes
    red = resort.slopes.red_slopes
    black = resort.slopes.black_slopes
    all_slopes = resort.slopes.all_slopes()
    resort_info = (
        f"{resort_name}\nRed: {red}, Blue: {blue}, Black: {black}, "
        f"All: {all_slopes}\nTop: {top_point} m, "
        f"Height difference: {height_difference} m"
    )
    return resort_info


def add_bookmarks_button(resort_name):
    keyboard = [
        [
            InlineKeyboardButton(
                "Add to bookmarks",
                callback_data=f"add_bookmarks:{resort_name}",
            )
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def resort_to_bookmarks(user_id, resort_id):
    print(f"MAKE TABLE WITH BOOKMARKS. user:{user_id}, resort:{resort_id}")
