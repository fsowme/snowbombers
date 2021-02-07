from django.core.paginator import Paginator
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from ski.models import Resort

from .models import User as django_user


class MyKeyboardMarkup(InlineKeyboardMarkup):
    @classmethod
    def de_queryset(cls, queryet, path, columns=3, keyboard=None):
        newkeyboard = []
        if keyboard:
            newkeyboard.extend(keyboard)
        paginator = Paginator(queryet, columns)
        for page in paginator:
            newkeyboard.append(
                [
                    InlineKeyboardButton(_.name, callback_data=f"{path}:{_.uuid}")
                    for _ in page
                ]
            )
        return cls(newkeyboard)

    def create_button(self, text, button_data, in_lust_row=False):
        if in_lust_row and len(self.inline_keyboard) != 0:
            self.inline_keyboard[-1].append(
                InlineKeyboardButton(text, callback_data=button_data)
            )
        else:
            self.inline_keyboard.append(
                [InlineKeyboardButton(text, callback_data=button_data)]
            )

    def add_button(self, button, in_lust_row=False):
        if in_lust_row and len(self.inline_keyboard) != 0:
            self.inline_keyboard[-1].append(button)
        else:
            self.inline_keyboard.append(button)


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


def button_add_bookmarks(resort_name, user_id=None):
    user = django_user.objects.get(telegram_id=user_id)
    if user.bookmarks.filter(uuid=resort_name).exists():
        button_text = "Remove from bookmarks"
        callback_data = f"bookmarks:del:{resort_name}"
    else:
        button_text = "Add to bookmarks"
        callback_data = f"bookmarks:add:{resort_name}"
    keyboard = [
        [
            InlineKeyboardButton(
                button_text,
                callback_data=callback_data,
            )
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
