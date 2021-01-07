import io
import os

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from rest_framework.parsers import JSONParser, json
from telegram import Bot, Update
from telegram.ext import CallbackQueryHandler, CommandHandler, Dispatcher

from .models import User as django_user
from .senders import button, resort_info, start

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)

dispatcher = Dispatcher(bot=bot, update_queue=None, workers=0)
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("info", resort_info))
dispatcher.add_handler(CallbackQueryHandler(button))


def index(request):
    return HttpResponse("Bot index")


def make_json(request_data):
    stream = io.BytesIO(request_data.body)
    update_object = JSONParser().parse(stream)
    update = Update(**update_object)
    return dict(update.message)


def check_user_start(user_data):
    user_id = int(user_data["id"])
    first_name = user_data["first_name"]
    is_bot = user_data["is_bot"]
    _, created = django_user.objects.get_or_create(
        telegram_id=user_id,
        defaults={"first_name": first_name, "is_bot": is_bot},
    )
    return created


@csrf_exempt
def webhook_updater(request):
    update = Update.de_json(json.loads(request.body), bot)
    dispatcher.process_update(update)
    return HttpResponse("Ok")


# @csrf_exempt
# def webhook_updater(request):
#     print(request.body)
#     new_message = make_json(request_data=request)
#     bot.send_message(chat_id=CHAT_ID, text="Hello")
#     if new_message["text"] == "/start":
#         user_info = new_message["from"]
#         if check_user_start(user_data=user_info):
#             bot.send_message(chat_id=CHAT_ID, text="You are registered")
#         else:
#             bot.send_message(
#                 chat_id=CHAT_ID, text="You are already registered"
#             )
#     return HttpResponse("Ok")
