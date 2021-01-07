from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot import parsers


def start(update, context):
    user_says = " ".join(context.args)
    print(context)
    update.message.reply_text("Hello! " + user_says + "!!!")
    # context.bot.send_message(
    #     chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    # )


def resort_info(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Asia", callback_data="1"),
            InlineKeyboardButton("Europe", callback_data="2"),
        ],
        [
            InlineKeyboardButton("North America", callback_data="3"),
            InlineKeyboardButton("South America", callback_data="4"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(f"Please choose:", reply_markup=reply_markup)


def button(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Selected: {query.data}")
