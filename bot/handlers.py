import os

from django.core.paginator import Paginator
from dotenv import load_dotenv
from ski.models import Continent, Country
from telegram import Bot, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    Dispatcher,
    Filters,
    MessageHandler,
)

from .bot_callbacks import button, select_continents, start

load_dotenv()
CONTINENT, COUNTRY, RESORT = range(1, 4)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

BOT = Bot(token=TELEGRAM_TOKEN)
DISPATCHER = Dispatcher(bot=BOT, update_queue=None, workers=0)
DISPATCHER.add_handler(CommandHandler("start", start))
DISPATCHER.add_handler(CommandHandler("info", select_continents))
DISPATCHER.add_handler(CallbackQueryHandler(button))


def continents_keyboard():
    paginator = Paginator(Country.objects.all().order_by("name"), 2)
    keyboard = []
    for page in paginator:
        keyboard.append(continent.name for continent in page)
    return keyboard


def start_test(update, context):
    reply_keyboard = [["Europe", "Asia"]]
    reply_keyboard = continents_keyboard()
    print(reply_keyboard)
    update.message.reply_text(
        "Select continent:",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True
        ),
    )
    return CONTINENT


def conv_select_continent(update, context):
    print("conv_select_continent:")
    print(update)
    land = update.message.text
    return COUNTRY


def conv_select_country(update, context):
    return RESORT


def conv_select_resort(update, context):
    return ConversationHandler.END


def conv_cancel(update, context):
    return ConversationHandler.END


resort_info = ConversationHandler(
    entry_points=[CommandHandler("test", start_test)],
    states={
        CONTINENT: [MessageHandler(Filters.text, conv_select_continent)],
        COUNTRY: [MessageHandler(Filters.text, conv_select_country)],
        RESORT: [MessageHandler(Filters.text, conv_select_resort)],
    },
    fallbacks=[CommandHandler("cancel", conv_cancel)],
)
DISPATCHER.add_handler(resort_info)
