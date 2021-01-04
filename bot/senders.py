from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def start(update, context):
    user_says = " ".join(context.args)
    print(context)
    update.message.reply_text("Hello! " + user_says + "!!!")
    # context.bot.send_message(
    #     chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    # )


def button_1():
    return "123"


def myline(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Mayrhofen", callback_data=button_1()),
            InlineKeyboardButton("Rosa Khutor", callback_data="2"),
        ],
        [InlineKeyboardButton("Val Thorans", callback_data="3")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Please choose:", reply_markup=reply_markup)


def button(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Selected: {query.data}")
