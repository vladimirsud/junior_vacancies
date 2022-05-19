import time
from threading import Thread

import schedule
import telebot
from telebot import types

import config
from handler_data import handler, prepare_mes
from hh_parsing import parse_data

bot = telebot.TeleBot(config.token)
list_data = []
chat_id = 0


def do_parse():
    bot.send_message(chat_id, str(time.time()))
    global list_data
    parsed_data = parse_data()
    list_data, data = handler(list_data, parsed_data)
    messages_data = prepare_mes(data)
    for i, v in messages_data.items():
        bot.send_message(chat_id, '\n'.join(v))


@bot.message_handler(commands=["start"])
def bot_start(message):
    global chat_id
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Проверить вакансию")
    markup.add(btn1)
    bot.send_message(chat_id, 'Бот запушен', reply_markup=markup)


@bot.message_handler(content_types=["text"])
def parse_vacancies(message):
    if message.text == "Проверить вакансию":
        first_message = True
        global list_data
        global chat_id
        chat_id = message.chat.id
        parsed_data = parse_data()
        list_data, data = handler(list_data, parsed_data)
        messages_data = prepare_mes(data)

        if not data:
            bot.send_message(message.chat.id, 'Нет новых данных')
            return
        if first_message:
            last_data_id = len(messages_data) - 1
            mes = f'Последняя вакансия\n\n'
            bot.send_message(message.chat.id, mes + '\n'.join(messages_data[last_data_id]))
        else:
            for i, v in messages_data.items():
                bot.send_message(message.chat.id, '\n'.join(v))


def run_bot():
    bot.polling()


def run_schedulers():
    schedule.every(10).minutes.do(do_parse)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    t1 = Thread(target=run_bot)
    t2 = Thread(target=run_schedulers)
    t1.start()
    t2.start()