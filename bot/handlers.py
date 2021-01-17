import os

from dotenv import load_dotenv
from telegram import Bot
from telegram.ext import CallbackQueryHandler, CommandHandler, Dispatcher

from .bot_callbacks import button, select_continents, start

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

BOT = Bot(token=TELEGRAM_TOKEN)
DISPATCHER = Dispatcher(bot=BOT, update_queue=None, workers=0)
DISPATCHER.add_handler(CommandHandler("start", start))
DISPATCHER.add_handler(CommandHandler("info", select_continents))
DISPATCHER.add_handler(CallbackQueryHandler(button))
