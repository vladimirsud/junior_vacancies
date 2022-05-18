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




def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(1)


def some_func():
    print(time.time())

@bot.message_handler(commands=["check"])
def repeat_all_messages(message):
    first_message = True
    global list_data

    parsed_data = parse_data()
    list_data, data = handler(list_data, parsed_data)
    messages_data = prepare_mes(data)

    if not data:
        bot.send_message(message.chat.id, 'Нет новых данных')

    if first_message:
        last_data_id = len(messages_data) - 1
        mes = f'Последняя вакансия\n\n'
        bot.send_message(message.chat.id, mes + '\n'.join(messages_data[last_data_id]))
    else:
        for i, v in messages_data.items():
            bot.send_message(message.chat.id, '\n'.join(v))


if __name__ == '__main__':
    schedule.every(5).seconds.do(some_func)
    Thread(target=schedule_checker).start()
    bot.infinity_polling()
