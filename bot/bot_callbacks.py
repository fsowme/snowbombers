from .keyboards import (
    add_bookmarks_button,
    check_user_start,
    continents_buttons,
    countries_buttons,
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
    if land_type == "start_info":
        return continents_buttons()
    if land_type == "continent":
        return countries_buttons(land_name)
    if land_type == "country":
        return resorts_buttons(land_name)
    raise ValueError("Unknown type of next step")


def manage_callback_info(update, context):
    pass


def manage_callback(update, context):
    query = update.callback_query
    query.answer()
    command = query.data
    if command.split(sep=":")[0] == "add_bookmarks":
        # 128609524
        user_id = query.message.chat.id
        resort_name = command.split(sep=":")[1]
        return resort_to_bookmarks(user_id=user_id, resort_name=resort_name)
    if command == "cancel":
        return update.callback_query.delete_message()
    if command.split(sep=":")[0] == "resort":
        resort_name = command.split(sep=":")[1]
        resort_info = get_resort_info(resort_name)
        return update.callback_query.message.reply_text(
            resort_info, reply_markup=add_bookmarks_button(resort_name)
        )
    reply_markup = choose_buttons(command)
    return query.edit_message_reply_markup(reply_markup=reply_markup)


def select_continents(update, context):
    reply_markup = continents_buttons()
    update.message.reply_text("Please choose:", reply_markup=reply_markup)
