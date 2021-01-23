import os

from dotenv import load_dotenv
from ski.models import Resort
from telegram import Bot, InlineKeyboardMarkup
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    Dispatcher,
)

from .bot_callbacks import button, select_continents, start
from .keyboards import continents_buttons, countries_buttons, resorts_buttons

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

BOT = Bot(token=TELEGRAM_TOKEN)
DISPATCHER = Dispatcher(bot=BOT, update_queue=None, workers=0)
DISPATCHER.add_handler(CommandHandler("start", start))
DISPATCHER.add_handler(CommandHandler("info", select_continents))
# DISPATCHER.add_handler(CallbackQueryHandler(button))

COUNTRY, RESORT, ANSWER = range(1, 4)


def send_continents(update, context):
    keyboard = continents_buttons()
    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    update.message.reply_text("Please choose:", reply_markup=reply_markup)
    return COUNTRY


def stop(update, context):
    return ConversationHandler.END


def send_countries(update, context):
    query = update.callback_query
    query.answer()
    keyboard = countries_buttons(continent_name=query.data)
    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    query.edit_message_reply_markup(reply_markup=reply_markup)
    return RESORT


def send_resorts(update, context):
    query = update.callback_query
    query.answer()
    keboard = resorts_buttons(country_name=query.data)
    reply_markup = InlineKeyboardMarkup(inline_keyboard=keboard)
    query.edit_message_reply_markup(reply_markup=reply_markup)
    return ANSWER


def send_resort_info(update, context):
    query = update.callback_query
    query.answer()
    text = resort_info(resort_name=query.data)
    query.message.reply_text(text)
    query.delete_message()
    return ConversationHandler.END


def resort_info(resort_name):
    resort = Resort.objects.get(name=resort_name)
    top_point = resort.top_point
    height_difference = resort.height_difference()
    blue = resort.slopes.blue_slopes
    red = resort.slopes.red_slopes
    black = resort.slopes.black_slopes
    all_slopes = resort.slopes.all_slopes()

    return (
        f"{resort_name}\nRed: {red}, Blue: {blue}, Black: {black}, "
        f"All: {all_slopes}\nTop: {top_point} m, "
        f"Height difference: {height_difference} m"
    )


conv_handler = ConversationHandler(
    entry_points=[CommandHandler("resort", send_continents)],
    states={
        COUNTRY: [CallbackQueryHandler(send_countries)],
        RESORT: [CallbackQueryHandler(send_resorts)],
        ANSWER: [CallbackQueryHandler(send_resort_info)],
    },
    fallbacks=[CommandHandler("stop", stop)],
    allow_reentry=True,
)

DISPATCHER.add_handler(conv_handler)
