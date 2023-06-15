import telebot
import psycopg2
from telebot import types
from config import TOKEN
from config import host, user, password, database

bot = telebot.TeleBot(TOKEN)

# подключение к базе данных (успешно)
connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

# Объявление переменных для викторины:
i = 0 # Счетчик номера вопроса
j = 1 # Счетчик сгоревших пуканов Саши
list_id_answers = [] # С писок ответов пользователя
q_count = 2 # Количество вопросов в базе
usr_id = 0
usr_nm = 0
usr_rev = 0



# Приветсвтие + представление Тимофея
@bot.message_handler(commands=['start'])
def start(message):

    with open('/Users/ksenia/Desktop/timosha.jpeg', 'rb') as T:
        bot.send_photo(message.chat.id, T)
    markup = types.InlineKeyboardMarkup(row_width=1)
    cont_btn = types.InlineKeyboardButton(text='Начать викторину 🦥', callback_data='start_quiz')
    no_btn = types.InlineKeyboardButton(text='А я не хочу ☹️', callback_data='dont_want')
    markup.add(cont_btn, no_btn)
    hello_txt = 'Привет🤗\n\nМеня зовут Тимофей и я манул🐱\nЯ являюсь символом Московского зоопарка с 1987 года😊\nИ сегодня я расскажу тебе кое-что интересное😏\n\nНо для начала предлагаю тебе пройти небольшую викторинку, тыкай на кнопку😁'
    bot.send_message(message.chat.id, hello_txt, reply_markup=markup)

# Декоратор с расчетом ответа
@bot.callback_query_handler(func=lambda call: True)
def please_start(call):
    global list_id_answers, i, q_count

    if call.data == 'dont_want':
        with open('/Users/ksenia/Desktop/angry_timosha.jpeg', 'rb') as A:
            bot.send_photo(call.message.chat.id, A)
        angry_text = '(Совет от разработчика)\nДавай не будем расстраивать Тимофея🥲\nи пройдем викторину, иначе он спрячется от посетителей зоопарка, и мы не сможем на него посмотреть☹️'
        markup = types.InlineKeyboardMarkup(row_width=1)
        reply = types.InlineKeyboardButton(text='Ладно, давай викторину😊', callback_data='start_quiz')
        markup.add(reply)
        bot.send_message(call.message.chat.id, angry_text, reply_markup=markup)

    elif call.data == 'start_quiz':
        i = 0
        list_id_answers = []
        bot.send_message(call.message.chat.id, text='Мурмяу🥰')
        quiz_body(call.message)

    elif call.data == 'answer1':
        list_id_answers.append(f'{i}.1')
        # i += 1
        quiz_body(call.message)
    elif call.data == 'answer2':
        list_id_answers.append(f'{i}.2')
        # i += 1
        quiz_body(call.message)
    elif call.data == 'answer3':
        list_id_answers.append(f'{i}.3')
        # i += 1
        quiz_body(call.message)
    elif call.data == 'answer4':
        list_id_answers.append(f'{i}.4')
        # i += 1
        quiz_body(call.message)

    elif call.data == 'results':

        with connection.cursor() as cursor:
            list_id_answers = str(list_id_answers)[1:-1]

            # вывод тотемного животного
            cursor.execute(f"Select case when a.grt = a.penguin then 'penguin' when a.grt = a.owl then 'penguin' when a.grt = a.bear then 'bear'  when a.grt = a.lori then 'lori'  when a.grt = a.irbis then 'irbis'  when a.grt = a.tiger then 'tiger'  when a.grt = a.eagle then 'eagle'  when a.grt = a.bird_sec then 'bird_sec'  when a.grt = a.vicuna then 'vicuna'  when a.grt = a.cuscus then 'cuscus'  when a.grt = a.crocodile then 'crocodile'  when a.grt = a.manul then 'manul'  when a.grt = a.seal then 'seal'  when a.grt = a.otter then 'otter'  end as animal from (select greatest(sum(penguin), sum(owl), sum(bear), sum(lori), sum(irbis), sum(tiger), sum(eagle), sum(bird_sec), sum(vicuna), sum(cuscus),   sum(crocodile), sum(manul), sum(seal), sum(otter)   ) as grt, sum(penguin) as penguin, sum(owl) as owl, sum(bear) as bear, sum(lori) as lori, sum(irbis) as irbis, sum(tiger) as tiger, sum(eagle) as eagle, sum(bird_sec) as bird_sec, sum(vicuna) as vicuna, sum(cuscus) as cuscus,  sum(crocodile) as crocodile, sum(manul) as manul, sum(seal) as seal, sum(otter) as otter from quiz where id_answer in({list_id_answers}) )a;")
            find_result = str(*cursor.fetchone())
            cursor.execute(f"select result_text from animal_results where id in ('{find_result}');")
            totemic_animal = str(*cursor.fetchone())
            cursor.execute(f"select image from animal_results where id in ('{find_result}');")
            totemic_image = str(*cursor.fetchone())
            bot.send_photo(call.message.chat.id, totemic_image)
            bot.send_message(call.message.chat.id, totemic_animal)
            # bot.send_message(call.message.chat.id, text='Ты пёс, а не суетолог.') # для Даши

            end_quiz(call.message)

        print(list_id_answers)

    # elif call.data == 'tell':
    #     bot.send_message(call.message.chat.id, text='Кинь мне денег на пожрать\n 5100 6914 8117 6513')
    #     end_quiz(call.message)

    elif call.data == 'review':
        bot.send_message(call.message.chat.id, text='Напиши свой отзыв и отправь мне☺️')
        bot.register_next_step_handler(call.message, get_review)

    elif call.data == 'send_review':
        send_review(call.message)
        bot.send_message(call.message.chat.id, 'Спасибо🐥')

    elif call.data == 'dont_send':
        markup = types.InlineKeyboardMarkup(row_width=1)
        change = types.InlineKeyboardButton('передумал☹️', callback_data='change mind')
        not_a_rev = types.InlineKeyboardButton('это не отзыв😬️', callback_data='not a review')
        text = 'Ты передумал отправлять свою оценку или это вовсе не отзыв?'
        markup.add(change, not_a_rev)
        bot.send_message(call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == 'change mind':
        photo = 'https://animals.pibig.info/uploads/posts/2023-04/1680790089' \
                '_animals-pibig-info-p-dikaya-koshka-manul-zhivotnie-instagram-1.jpg'
        bot.send_photo(call.message.chat.id, photo)
        text = 'Очень жаль, ведь твое мнение очень важно для меня🥺'
        bot.send_message(call.message.chat.id, text=text)

    elif call.data == 'not a review':
        dont_type(call.message)

    elif call.data == 'friends':
        photo = 'https://cs14.pikabu.ru/post_img/big/2022/07/06/7/1657106773137619411.jpg'
        link = 'https://www.justbenice.ru/work/moscowzoo/'
        text = 'Помнишь я обещал рассказать тебе кое-что интересное?\n\n' \
               'Так вот, зоопарк предоставляет возможность стать настоящим опекуном ' \
               'твоего тотемного животного😱(либо любого другого вида)\n\n' \
               'Уже долгое время действует программа "Клуб Друзей", ты можешь' \
               'почитать о ней и задать вопросы организаторам тут👇🏻'
        markup = types.InlineKeyboardMarkup(row_width=2)
        site = types.InlineKeyboardButton('Сайт', url=link)
        contacts = types.InlineKeyboardButton('Контакты', callback_data='contacts')
        markup.add(site, contacts)
        bot.send_photo(call.message.chat.id, photo)
        bot.send_message(call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == 'contacts':
        text = 'Как только мне сообщат контактные данные, они тут же появятся здесь🤗'
        bot.send_message(call.message.chat.id, text=text)


@bot.message_handler(content_types=['text'])
def quiz_body(message : False):

        with connection.cursor() as cursor:

            # достаем максимальный id вопроса
            global i, q_count
            cursor.execute('select max(id_question) from quiz')  # запрашиваем кортеж с максимальным id
            q_count = (cursor.fetchone())[0]  # достаем его из бд и присваиваем его значение переменной

            i += 1

            if i <= q_count:

                # достаем вопрос из базы данных
                cursor.execute(f'select question from quiz where id_question = {i}')
                question = cursor.fetchone()

                # достаем ответы по id_answer из БД
                cursor.execute(f'select answer from quiz where id_answer = {i}.1')
                answer_text1 = str(*cursor.fetchone())
                cursor.execute(f'select answer from quiz where id_answer = {i}.2')
                answer_text2 = str(*cursor.fetchone())
                cursor.execute(f'select answer from quiz where id_answer = {i}.3')
                answer_text3 = str(*cursor.fetchone())
                cursor.execute(f'select answer from quiz where id_answer = {i}.4')
                answer_text4 = str(*cursor.fetchone())

                # назначаем кнопки
                markup = types.InlineKeyboardMarkup(row_width=1)
                btn1 = types.InlineKeyboardButton(text=answer_text1, callback_data='answer1')
                btn2 = types.InlineKeyboardButton(text=answer_text2, callback_data='answer2')
                btn3 = types.InlineKeyboardButton(text=answer_text3, callback_data='answer3')
                btn4 = types.InlineKeyboardButton(text=answer_text4, callback_data='answer4')
                markup.add(btn1, btn2, btn3, btn4)
                bot.send_message(message.chat.id, *question, reply_markup=markup)

            else:
                results = 'Кажется, я знаю, кто ты на самом деле😏\nГотов узнать?'
                markup = types.InlineKeyboardMarkup(row_width=1)
                res = types.InlineKeyboardButton(text='Конечно😍', callback_data='results')
                markup.add(res)
                bot.send_message(message.chat.id, results, reply_markup=markup)

def end_quiz(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    restart = types.InlineKeyboardButton(text='Хочу еще разочек🧐', callback_data='start_quiz')
    review = types.InlineKeyboardButton(text='Оставить отзыв📌', callback_data='review')
    post = types.InlineKeyboardButton(text='Поделиться в VK 💭', url='https://vk.com/share.php?url=https://t.me/zoohobbit_bot)')
    friends = types.InlineKeyboardButton(text='Тыкни сюда🙃', callback_data='friends')
    markup.add(restart, review, post, friends)
    text = 'Ты крут! Как тебе викторина?😏'
    bot.send_message(message.chat.id, text=text, reply_markup=markup)

def get_review(message):
    global usr_nm, usr_id, usr_rev
    markup = types.InlineKeyboardMarkup(row_width=2)
    send = types.InlineKeyboardButton(text='да', callback_data='send_review')
    dont_send = types.InlineKeyboardButton(text='нет', callback_data='dont_send')
    markup.add(send, dont_send)
    usr_id = message.from_user.id
    usr_nm = message.from_user.username
    usr_rev = message.text
    bot.send_message(message.chat.id, text='Отправляю твою оценку?😊', reply_markup=markup)

def send_review(message):
    global usr_nm, usr_id, usr_rev
    review_user_id = usr_id
    review_user = usr_nm
    review_text = usr_rev
    cursor = connection.cursor()
    cursor.execute(f"insert into reviews (id_user, username, review) values ('{review_user_id}','{review_user}','{review_text}')")
    print(review_user_id, review_text)
    connection.commit()

def dont_type(message):
    if message.text:
        photo = 'https://animals.pibig.info/uploads/posts/2023-04/1680790089_animals-pibig-info-p-dikaya-koshka-manul-zhivotnie-instagram-1.jpg'
        bot.send_photo(message.chat.id, photo)
        text = 'Пожалуйста, не пиши мне ничего🙏🏻\n' \
               'Мои смотрители еще не научили меня понимать человеческую речь, но я в процессе😁\n' \
               'И уже могу собирать отзывы, но для этого необходимо нажать соответствующую кнопку, ' \
               'когда она у тебя появится🙃'
        bot.send_message(message.chat.id, text=text)


bot.polling(none_stop=True)
