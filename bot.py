import telebot
import config
import schedule
import time
from threading import Thread
from hh_parsing import parse_data
from handler_data import handler, prepare_mes

bot = telebot.TeleBot(config.token)
chat_id = 0
list_data = []


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




if __name__ == '__main__':
    schedule.every(5).seconds.do(some_func)
    Thread(target=schedule_checker).start()
    bot.infinity_polling()
