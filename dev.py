import telebot
# import psycopg2
from telebot import types
from urls import *
from extensions import *
from texts import *

bot = telebot.TeleBot('6104965414:AAE-qI0waYJYnUxIodQGONHTs6gYAUUEKQM')

@bot.message_handler(commands=['start'])
# приветственное сообщение
def start(message):

    markup = types.InlineKeyboardMarkup(row_width=1)
    cont_btn = types.InlineKeyboardButton(start_quiz, callback_data='start quiz')
    no_btn = types.InlineKeyboardButton(dont_want, callback_data='dont want')
    markup.add(cont_btn, no_btn)

    bot.send_photo(message.chat.id, photo=hello_manul)
    bot.send_message(message.chat.id, hello, reply_markup=markup)

i = 1 # счетчик индекса вопросов викторины

# основная функция с викториной
@bot.message_handler(regexp='')
def quiz(message):
    global i

    try:
        q, an1, an2, an3, an4 = Quiz.questions(i)

        markup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton(text=str(an1), callback_data='an1')
        btn2 = types.InlineKeyboardButton(text=str(an2), callback_data='an2')
        btn3 = types.InlineKeyboardButton(text=str(an3), callback_data='an3')
        btn4 = types.InlineKeyboardButton(text=str(an4), callback_data='an4')
        markup.add(btn1, btn2, btn3, btn4)

        bot.send_message(message.chat.id, text=q, reply_markup=markup)

    except ValueError as e:
        bot.send_message(message.chat.id, 'Прости, на этом пока что все :(')
        print(f'[INFO] {e}')

    except QuizException:
        pass


@bot.callback_query_handler(func= lambda call: True)
def callbacks(call):
    global i

    # викторина
    if call.data == 'start quiz':
        quiz(call.message)

    elif call.data == 'an1':
        i += 1
        quiz(call.message)

    elif call.data == 'an2':
        i += 1
        quiz(call.message)

    elif call.data == 'an3':
        i += 1
        quiz(call.message)

    elif call.data == 'an4':
        i += 1
        quiz(call.message)

    # остальные колбэки
    elif call.data == 'dont want':

        markup = types.InlineKeyboardMarkup(row_width=1)
        reply = types.InlineKeyboardButton(okay_quiz, callback_data='start quiz')
        markup.add(reply)

        bot.send_photo(call.message.chat.id, angry_manul)
        bot.send_message(call.message.chat.id, angry, reply_markup=markup)

bot.polling(none_stop=True)
