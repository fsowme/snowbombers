from ski.models import Continent, Country, Resort
from telegram import InlineKeyboardMarkup

from .keyboards import continents_buttons, countries_buttons, resorts_buttons


def start(update, context):
    user_says = " ".join(context.args)
    update.message.reply_text("Hello! " + user_says + "!!!")
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


def choose_buttons(update):
    land = update.callback_query.data
    if Continent.objects.filter(name=land):
        return countries_buttons(land)
    if Country.objects.filter(name=land):
        return resorts_buttons(land)
    raise ValueError("Unknown region")


def button(update, context):
    land = update.callback_query.data
    if Resort.objects.filter(name=land):
        resort = Resort.objects.get(name=land)
        name = land
        top_point = resort.top_point
        height_difference = resort.height_difference()
        blue = resort.slopes.blue_slopes
        red = resort.slopes.red_slopes
        black = resort.slopes.black_slopes
        all_slopes = resort.slopes.all_slopes()

        update.callback_query.message.reply_text(
            f"{name}\nRed: {red}, Blue: {blue}, Black: {black}, "
            f"All: {all_slopes}\nTop: {top_point} m, "
            f"Height difference: {height_difference} m"
        )
        print(update)
        return update.callback_query.delete_message()
    keyboard = choose_buttons(update)
    query = update.callback_query
    query.answer()
    reply_markup = InlineKeyboardMarkup(keyboard)
    return query.edit_message_reply_markup(reply_markup=reply_markup)


def select_continents(update, context):
    keyboard = continents_buttons()
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Please choose:", reply_markup=reply_markup)


def select_countries(update, context):
    keyboard = countries_buttons(update.callback_query.data)
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Please choose:", reply_markup=reply_markup)
