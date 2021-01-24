import os

from dotenv import load_dotenv
from telegram import Bot
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    Dispatcher,
    Filters,
    MessageHandler,
)

from .bot_callbacks import (
    available_commands,
    manage_callback,
    select_continents,
    start,
)

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

BOT = Bot(token=TELEGRAM_TOKEN)
DISPATCHER = Dispatcher(bot=BOT, update_queue=None, workers=0)
DISPATCHER.add_handler(CommandHandler("start", start))
DISPATCHER.add_handler(CommandHandler("info", select_continents))
DISPATCHER.add_handler(CallbackQueryHandler(manage_callback))
DISPATCHER.add_handler(MessageHandler(Filters.all, available_commands))
