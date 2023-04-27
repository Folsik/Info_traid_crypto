import telebot
from telebot import types
from currency_converter import CurrencyConverter

bot = telebot.TeleBot('') # Токен
currency = CurrencyConverter()
amount = 0


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Сумма конвертации: ")
    bot.register_next_step_handler(message, summa)


def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат ввода")
        bot.register_next_step_handler(message, summa)
        return
    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        button_1 = types.InlineKeyboardButton("USD/EUR", callback_data="usd/eur")
        button_2 = types.InlineKeyboardButton("EUR/USD", callback_data="eur/usd")
        button_3 = types.InlineKeyboardButton("USD/GBP", callback_data="usd/gbp")
        button_4 = types.InlineKeyboardButton("Другое ", callback_data="else")
        markup.add(button_1, button_2, button_3, button_4)
        bot.send_message(message.chat.id, "Пара валют", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Только числа больше 0")
        bot.register_next_step_handler(message, summa)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call .data != "else":
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Итог: {round(res, 2)}. Можешь написать следующую сумму')
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, "Валютная пара через '/'")
        bot.register_next_step_handler(call.message, mycurrency)


def mycurrency(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Итог: {round(res, 2)}. Можешь написать следующую сумму')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, "Ты по моему перепутал")
        bot.register_callback_query_handler(message, mycurrency)


bot.polling(none_stop=True)