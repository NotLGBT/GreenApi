import telebot
from telebot import types  

bot = telebot.TeleBot('************************************')

@bot.message_handler(commands=['start'])
def start(message):

    confirm_button = types.InlineKeyboardButton(
        text="Confirm", 
        web_app=types.WebAppInfo(url="https://10.96.0.54:5000")
    )
    deny_button = types.InlineKeyboardButton(
        text="Deny", 
        callback_data="decline"
    )


    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(confirm_button, deny_button)


    bot.send_message(
        message.chat.id, 
        'Please confirm terms of use', 
        reply_markup=keyboard
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "decline":
        bot.send_message(call.message.chat.id, "You declined the terms of use.")
    elif call.data == "agree":
        bot.send_message(call.message.chat.id, "Thank you for agreeing to the terms of use!")


@bot.message_handler(commands=['stop'])
def stop(message):
    bot.send_message(message.chat.id, 'All activity stopped')


bot.polling()

