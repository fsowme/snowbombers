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

from bot.bot_callbacks import (
    available_commands,
    bookmarks,
    cancel,
    info,
    print_callback,
    search,
    start,
)

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

BOT = Bot(token=TELEGRAM_TOKEN)
DISPATCHER = Dispatcher(bot=BOT, update_queue=None, workers=0)
DISPATCHER.add_handler(CommandHandler("start", start))

DISPATCHER.add_handler(CommandHandler("info", info))
DISPATCHER.add_handler(CallbackQueryHandler(info, pattern="^info"))

DISPATCHER.add_handler(CommandHandler("bookmarks", bookmarks))
DISPATCHER.add_handler(CallbackQueryHandler(bookmarks, pattern="^bookmarks"))

DISPATCHER.add_handler(CommandHandler("search", search))
DISPATCHER.add_handler(CallbackQueryHandler(search, pattern="^search"))

DISPATCHER.add_handler(CallbackQueryHandler(cancel, pattern="^cancel$"))
DISPATCHER.add_handler(MessageHandler(Filters.all, available_commands))
DISPATCHER.add_handler(CallbackQueryHandler(print_callback))
