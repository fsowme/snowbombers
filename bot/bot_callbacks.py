from ski.models import Continent, Country, Resort

from .keyboards import (
    MyKeyboardMarkup,
    add_bookmarks_button,
    check_user_start,
    continents_buttons,
    countries_buttons,
    del_resort_from_bookmarks,
    get_resort_info,
    resort_to_bookmarks,
    resorts_buttons,
    resorts_in_bookmarks,
)


def available_commands(update, context):
    answer = (
        "/start - start to conversation\n "
        "/info - search resort by regions\n "
        "/bookmarks - manage your bookmarks"
    )
    return update.message.reply_text(answer)


def start(update, context):
    username = update.message.from_user.first_name
    check_user_start(user_data=update.message.from_user)
    update.message.reply_text(f"Hello {username}!")
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )
    return available_commands(update, context)


def manage_bookmarks(update, context):
    user_id = update.message.from_user.id
    reply_markup = resorts_in_bookmarks(user_id=user_id)
    update.message.reply_text("Please choose:", reply_markup=reply_markup)


def choose_buttons(next_step):
    land_type, land_name = next_step.split(sep=":")
    if land_type == "info_start":
        return continents_buttons()
    if land_type == "info_continent":
        return countries_buttons(land_name)
    if land_type == "info_country":
        return resorts_buttons(land_name)
    raise ValueError("Unknown type of next step")


def manage_callback(update, context):
    # print(update)
    query = update.callback_query
    query.answer()
    command = query.data
    user_id = query.message.chat.id

    if command.split(sep=":")[0] == "bookmarks_add":
        resort_name = command.split(sep=":")[1]
        resort_to_bookmarks(user_id=user_id, resort_name=resort_name)
        command = f"info_resort:{resort_name}"
        return query.edit_message_reply_markup(
            reply_markup=add_bookmarks_button(resort_name, user_id)
        )
    if command.split(sep=":")[0] == "bookmarks_del":
        resort_name = command.split(sep=":")[1]
        del_resort_from_bookmarks(user_id=user_id, resort_name=resort_name)
        return query.edit_message_reply_markup(
            reply_markup=add_bookmarks_button(resort_name, user_id)
        )

    if command.split(sep=":")[0] == "info_resort":
        uuid = command.split(sep=":")[1]
        resort_info = get_resort_info(uuid)
        return query.message.reply_text(
            resort_info, reply_markup=add_bookmarks_button(uuid, user_id)
        )
    reply_markup = choose_buttons(command)
    return query.edit_message_reply_markup(reply_markup=reply_markup)


def cancel(update, context):
    update.callback_query.answer()
    return update.callback_query.delete_message()


def manage_info_conversation(update, context):
    if update.message and update.message.text == "/info":
        queryset = Continent.objects.all()
        markup = MyKeyboardMarkup.de_queryset(queryet=queryset, path="info:continent")
        markup.create_button(text="Quit", button_data="cancel")
        return update.message.reply_text(text="Please choose:", reply_markup=markup)
    query = update.callback_query
    command, parent, parent_uuid = query.data.split(sep=":")
    print(f"{command}_{parent}_{parent_uuid}")

    if parent == "start":
        queryset = Continent.objects.all()
        markup = MyKeyboardMarkup.de_queryset(queryet=queryset, path="info:continent")
        markup.create_button(text="Quit", button_data="cancel")
        query.answer()
        return query.edit_message_reply_markup(reply_markup=markup)
    if parent == "continent":
        queryset = Country.objects.filter(continent__uuid=parent_uuid)
        markup = MyKeyboardMarkup.de_queryset(queryet=queryset, path="info:country")
        markup.create_button(text="Quit", button_data="cancel")
        markup.create_button(text="Back to continents", button_data="info:start:")
        query.answer()
        return query.edit_message_reply_markup(reply_markup=markup)
    if parent == "country":
        queryset = Resort.objects.filter(country__uuid=parent_uuid)
        back_uuid = Continent.objects.get(countries__uuid=parent_uuid).uuid
        markup = MyKeyboardMarkup.de_queryset(queryet=queryset, path="info:resort")
        markup.create_button(text="Quit", button_data="cancel")
        markup.create_button(
            text="Back to countries", button_data=f"info:continent:{back_uuid}"
        )
        query.answer()
        return query.edit_message_reply_markup(reply_markup=markup)
    if parent == "resort":
        user_id = query.message.chat.id
        answer = get_resort_info(uuid=parent_uuid)
        query.answer()
        return query.message.reply_text(
            answer, reply_markup=add_bookmarks_button(parent_uuid, user_id)
        )
