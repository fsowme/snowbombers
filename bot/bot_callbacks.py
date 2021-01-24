from ski.models import Continent, Country, Resort
from telegram import InlineKeyboardMarkup

from .keyboards import continents_buttons, countries_buttons, resorts_buttons


def start(update, context):
    user_says = " ".join(context.args)
    update.message.reply_text("Hello! " + user_says + "!!!")
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


def choose_buttons(next_step):
    land_type, land_name = next_step.split(sep=":")
    if land_type == "start_info":
        return continents_buttons()
    if land_type == "continent":
        return countries_buttons(land_name)
    if land_type == "country":
        return resorts_buttons(land_name)
    raise ValueError("Unknown next step")


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


def button(update, context):
    query = update.callback_query
    query.answer()
    land = query.data
    if land.split(sep=":")[0] == "resort":
        resort_name = land.split(sep=":")[1]
        update.callback_query.message.reply_text(get_resort_info(resort_name))
        return update.callback_query.delete_message()
    keyboard = choose_buttons(land)
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
