import psycopg2
from config import host, user, database, password

'''
В ЭТОМ ФАЙЛЕ ОБЪЯВЛЯЮТСЯ ВСЕ КЛАССЫ И ПЕРЕМЕННЫЕ, СОДЕРЖАЩИЕ ДАННЫЕ ИЗ БАЗЫ
'''

# подключение к базе данных (успешно)
connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
cur = connection.cursor()

# максимальный id_question
def max_id():
    cur.execute('select max(id_question) from quiz')
    max_id_q = int(str(*cur.fetchone()))
    return max_id_q

class Quiz:
    @staticmethod
    def questions(i):

        max_id_q = max_id()

        if i <= max_id_q:
            cur.execute(f'select question from quiz where id_question = {i}')
            q = str(*cur.fetchone())
            yield q

            cur.execute(f'select answer from quiz where id_answer = {i}.1')
            an1 = str(*cur.fetchone())
            yield an1

            cur.execute(f'select answer from quiz where id_answer = {i}.2')
            an2 = str(*cur.fetchone())
            yield an2

            cur.execute(f'select answer from quiz where id_answer = {i}.3')
            an3 = str(*cur.fetchone())
            yield an3

            cur.execute(f'select answer from quiz where id_answer = {i}.4')
            an4 = str(*cur.fetchone())
            yield an4

            i += 1

        else:
            pass

class QuizException(BaseException):
    pass
