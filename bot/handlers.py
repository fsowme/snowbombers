import os
import re

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
    cancel,
    manage_bookmarks,
    manage_callback,
    manage_info_conversation,
    start,
)

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

BOT = Bot(token=TELEGRAM_TOKEN)
DISPATCHER = Dispatcher(bot=BOT, update_queue=None, workers=0)
DISPATCHER.add_handler(CommandHandler("start", start))

DISPATCHER.add_handler(CommandHandler("info", manage_info_conversation))
DISPATCHER.add_handler(CallbackQueryHandler(manage_info_conversation, pattern="^info"))

DISPATCHER.add_handler(CommandHandler("bookmarks", manage_bookmarks))
DISPATCHER.add_handler(CallbackQueryHandler(manage_callback, pattern="^bookmarks"))

DISPATCHER.add_handler(CallbackQueryHandler(cancel, pattern="^cancel$"))
DISPATCHER.add_handler(MessageHandler(Filters.all, available_commands))
