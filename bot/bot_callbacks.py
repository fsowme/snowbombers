from django.db.models.expressions import F
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton

from bot.keyboards import (
    MyKeyboardMarkup,
    button_add_bookmarks,
    get_resort_info,
    markup_start_search,
)
from bot.models import User as User
from ski.models import Continent, Country, Resort


def available_commands(update, context):
    answer = (
        "/start - start to conversation\n "
        "\n "
        "/info - search resort by regions\n "
        "\n "
        "/bookmarks - manage your bookmarks\n "
        "\n "
        "/search - search by parameters"
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
        reply_markup = MyKeyboardMarkup.de_queryset(queryet=queryset, path="info:resort:")
        reply_markup.create_button(text="Quit", button_data="cancel")
        return update.message.reply_text("Please choose:", reply_markup=reply_markup)

    query = update.callback_query
    entrypoint, command, resort_uuid = query.data.split(sep=":")
    resort = Resort.objects.get(uuid=resort_uuid)
    user_id = query.message.chat_id
    if command == "del":
        User.objects.get(telegram_id=user_id).bookmarks.remove(resort)
        text, callback_data = "Add to bookmarks", f"bookmarks:add:{resort_uuid}"
    else:  # command == "add":
        User.objects.get(telegram_id=user_id).bookmarks.add(resort)
        text, callback_data = "Remove from bookmarks", f"bookmarks:del:{resort_uuid}"
    markup = MyKeyboardMarkup(
        [[InlineKeyboardButton(text=text, callback_data=callback_data)]]
    )
    query.edit_message_reply_markup(reply_markup=markup)
    return query.answer()


def info(update, context):
    if update.message and update.message.text == "/info":
        queryset = Continent.objects.all()
        markup = MyKeyboardMarkup.de_queryset(queryet=queryset, path="info:continent:")
        markup.create_button(text="Quit", button_data="cancel")
        return update.message.reply_text(text="Please choose:", reply_markup=markup)

    query = update.callback_query
    entrypoint, parent_land, parent_uuid = query.data.split(sep=":")
    if parent_land == "resort":
        user_id = query.message.chat.id
        answer = get_resort_info(uuid=parent_uuid)
        query.message.reply_text(
            answer, reply_markup=button_add_bookmarks(parent_uuid, user_id)
        )
        return query.answer()
    if parent_land == "start":
        queryset = Continent.objects.all()
        markup = MyKeyboardMarkup.de_queryset(queryet=queryset, path="info:continent:")
    elif parent_land == "continent":
        queryset = Country.objects.filter(continent__uuid=parent_uuid)
        markup = MyKeyboardMarkup.de_queryset(queryet=queryset, path="info:country:")
        markup.create_button(text="Back", button_data="info:start:")
    else:  # parent_land == "country":
        queryset = Resort.objects.filter(country__uuid=parent_uuid)
        back_uuid = Continent.objects.get(countries__uuid=parent_uuid).uuid
        markup = MyKeyboardMarkup.de_queryset(queryet=queryset, path="info:resort:")
        markup.create_button(text="Back", button_data=f"info:continent:{back_uuid}")
    markup.create_button(text="Quit", button_data="cancel")
    query.edit_message_reply_markup(reply_markup=markup)
    return query.answer()


def search(update, context):
    if update.message and update.message.text == "/search":
        return update.message.reply_text(
            text="Please choose:", reply_markup=markup_start_search()
        )

    query = update.callback_query
    entrypoint, parameter, values = query.data.split(sep=":")

    last_button_data = query.message.reply_markup.inline_keyboard[-1][-1].callback_data
    apply_button = False
    if last_button_data.split(sep=":")[0] == "apply":
        apply_button = True
        apply_data = last_button_data
    if parameter == "name":
        pass
    elif parameter == "height_difference":
        pass
    elif parameter == "top_point":
        pass
    elif parameter == "length_all_slopes":
        pass
    elif parameter == "region":
        if values == "start":
            queryset = Continent.objects.all()
            path = "search:region:continent="
            markup = MyKeyboardMarkup.de_queryset(queryet=queryset, path=path)
            if apply_button:
                markup.create_button(text="Apply", button_data=apply_data)
            query.edit_message_reply_markup(reply_markup=markup)
            return query.answer()

        elif values.split(sep="=")[0] == "continent":
            continent_uuid = values.split(sep="=")[1]
            continent_name = Continent.objects.get(uuid=continent_uuid).name
            queryset = Country.objects.filter(continent__uuid=continent_uuid)
            path = "search:region:country="
            markup = MyKeyboardMarkup.de_queryset(queryet=queryset, path=path)
            search_data = f"search:now:continent={continent_uuid}"
            markup.create_button(
                text=f"Add {continent_name} to filter", button_data=search_data
            )
            if apply_button:
                markup.create_button(text="Apply", button_data=apply_data)
            query.edit_message_reply_markup(reply_markup=markup)
            return query.answer()
        else:  # values.split(sep="=")[0] == "country":
            country_uuid = values.split(sep="=")[1]
            country_name = Country.objects.get(uuid=country_uuid).name
            search_data = f"search:now:country={country_uuid}"
            markup = MyKeyboardMarkup.from_button(
                InlineKeyboardButton(
                    text=f"Add {country_name} to filter", callback_data=search_data
                )
            )
            if apply_button:
                markup.create_button(text="Apply", button_data=apply_data)
            query.edit_message_reply_markup(reply_markup=markup)
            return query.answer()

    else:  # parameter == "now"
        if apply_button:
            filter = apply_data + "&" + values

        else:
            filter = f"apply:{values}"

        markup = markup_start_search(
            apply_button=[InlineKeyboardButton(text="Apply", callback_data=filter)]
        )
        query.edit_message_reply_markup(reply_markup=markup)
        return query.answer()


def search_res(height_difference=None, top_point=None, length_all_slopes=None):
    queryset = Resort.objects.all()
    if height_difference:
        queryset = queryset.annotate(diff=F("top_point") - F("bottom_point"))
        queryset = queryset.filter(diff__gt=height_difference[0]).filter(
            diff__lt=height_difference[1]
        )
    if top_point:
        queryset = queryset.filter(top_point__gt=top_point)
    return queryset


def print_callback(update, context):
    query = update.callback_query
    params = {}
    for param in query.data.split(":")[1].split("&"):
        param_type, uuid = param.split("=")
        if params.get(param_type):
            params[param_type].append(uuid)
        else:
            params[param_type] = [uuid]

    queryset = Resort.objects.all()
    filters = query.data.split(":")[1].split("&")
    for filter in filters:
        land, uuid = filter.split("=")
        if land == "continent":
            queryset = queryset.filter(continent__uuid=uuid)
        if land == "country":
            queryset = queryset.filter(country__uuid=uuid)
    markup = MyKeyboardMarkup.de_queryset(queryet=queryset, path="info:resort:")
    query.edit_message_reply_markup(reply_markup=markup)
    return query.answer()
