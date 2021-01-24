from telegram import InlineKeyboardMarkup

from .keyboards import (
    continents_buttons,
    countries_buttons,
    get_resort_info,
    resorts_buttons,
)


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
    raise ValueError("Unknown type of next step")


def button(update, context):
    query = update.callback_query
    query.answer()
    command = query.data
    if command == "cancel":
        return update.callback_query.delete_message()
    if command.split(sep=":")[0] == "resort":
        resort_info = get_resort_info(command.split(sep=":")[1])
        return update.callback_query.message.reply_text(resort_info)
    keyboard = choose_buttons(command)
    reply_markup = InlineKeyboardMarkup(keyboard)
    return query.edit_message_reply_markup(reply_markup=reply_markup)


def select_continents(update, context):
    keyboard = continents_buttons()
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Please choose:", reply_markup=reply_markup)
