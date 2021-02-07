from bot.models import User as User
from ski.models import Continent, Country, Resort

from .keyboards import MyKeyboardMarkup, button_add_bookmarks, get_resort_info


def available_commands(update, context):
    answer = (
        "/start - start to conversation\n "
        "/info - search resort by regions\n "
        "/bookmarks - manage your bookmarks"
    )
    return update.message.reply_text(answer)


def start(update, context):
    telegram_id = update.message.from_user.id
    first_name = update.message.from_user.first_name
    is_bot = update.message.from_user.is_bot
    User.objects.get_or_create(
        telegram_id=telegram_id, defaults={"first_name": first_name, "is_bot": is_bot}
    )
    update.message.reply_text(f"Hello {first_name}!")
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )
    return available_commands(update, context)


def cancel(update, context):
    update.callback_query.answer()
    return update.callback_query.delete_message()


def bookmarks(update, context):
    if update.message and update.message.text == "/bookmarks":
        user_id = update.message.from_user.id
        queryset = User.objects.get(telegram_id=user_id).bookmarks.all()
        reply_markup = MyKeyboardMarkup.de_queryset(queryet=queryset, path="info:resort")
        reply_markup.create_button(text="Quit", button_data="cancel")
        return update.message.reply_text("Please choose:", reply_markup=reply_markup)

    query = update.callback_query
    entrypoint, command, resort_uuid = query.data.split(sep=":")
    resort = Resort.objects.get(uuid=resort_uuid)
    user_id = query.message.chat_id
    if command == "del":
        User.objects.get(telegram_id=user_id).bookmarks.remove(resort)
    if command == "add":
        User.objects.get(telegram_id=user_id).bookmarks.add(resort)
    query.edit_message_reply_markup(
        reply_markup=button_add_bookmarks(resort_uuid, user_id)
    )
    return query.answer()


def manage_info_conversation(update, context):
    if update.message and update.message.text == "/info":
        queryset = Continent.objects.all()
        markup = MyKeyboardMarkup.de_queryset(queryet=queryset, path="info:continent")
        markup.create_button(text="Quit", button_data="cancel")
        return update.message.reply_text(text="Please choose:", reply_markup=markup)
    query = update.callback_query
    entrypoint, parent_land, parent_uuid = query.data.split(sep=":")

    if parent_land == "start":
        queryset = Continent.objects.all()
        markup = MyKeyboardMarkup.de_queryset(queryet=queryset, path="info:continent")
        markup.create_button(text="Quit", button_data="cancel")
        query.answer()
        return query.edit_message_reply_markup(reply_markup=markup)
    if parent_land == "continent":
        queryset = Country.objects.filter(continent__uuid=parent_uuid)
        markup = MyKeyboardMarkup.de_queryset(queryet=queryset, path="info:country")
        markup.create_button(text="Quit", button_data="cancel")
        markup.create_button(text="Back to continents", button_data="info:start:")
        query.answer()
        return query.edit_message_reply_markup(reply_markup=markup)
    if parent_land == "country":
        queryset = Resort.objects.filter(country__uuid=parent_uuid)
        back_uuid = Continent.objects.get(countries__uuid=parent_uuid).uuid
        markup = MyKeyboardMarkup.de_queryset(queryet=queryset, path="info:resort")
        markup.create_button(text="Quit", button_data="cancel")
        markup.create_button(
            text="Back to countries", button_data=f"info:continent:{back_uuid}"
        )
        query.answer()
        return query.edit_message_reply_markup(reply_markup=markup)
    if parent_land == "resort":
        user_id = query.message.chat.id
        answer = get_resort_info(uuid=parent_uuid)
        query.answer()
        return query.message.reply_text(
            answer, reply_markup=button_add_bookmarks(parent_uuid, user_id)
        )
