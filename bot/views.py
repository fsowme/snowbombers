import io
import logging
import os

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from rest_framework.parsers import JSONParser
from telegram import Bot, Update, User

from .models import User

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


bot_logger = logging.getLogger(__name__)
bot = Bot(token=TELEGRAM_TOKEN)


def index(request):
    return HttpResponse("Bot index")


def make_json(request_data):
    stream = io.BytesIO(request_data.body)
    update_object = JSONParser().parse(stream)
    update = Update(**update_object)
    return dict(update.message)


def start(user_data):
    user_id = int(user_data["id"])
    first_name = user_data["first_name"]
    is_bot = user_data["is_bot"]
    _, created = User.objects.get_or_create(
        telegram_id=user_id,
        defaults={"first_name": first_name, "is_bot": is_bot},
    )
    return created


@csrf_exempt
def webhook_updater(request):
    new_message = make_json(request_data=request)
    bot.send_message(chat_id=CHAT_ID, text="Hello")
    if new_message["text"] == "/start":
        user_info = new_message["from"]
        if start(user_data=user_info):
            bot.send_message(chat_id=CHAT_ID, text="You are registered")
        else:
            bot.send_message(
                chat_id=CHAT_ID, text="You are already registered"
            )
    return HttpResponse("Ok")
