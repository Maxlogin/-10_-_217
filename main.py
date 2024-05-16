import telebot
import sqlite3
import random
import csv
TOKEN = '6758181956:AAGpdPEiF9Ae-FNNg95X3bZ0OYUmhEGQvvU'

bot = telebot.TeleBot(TOKEN)

jokes = [
    "Почему программисты всегда путают Хэллоуин и Рождество? Потому что 31 октября равно 25 декабря.",
    "Как называют программиста, который использует только одну функцию? Специалист.",
    "Как называется идеальное место для программиста? База данных.",
    "Почему программисты любят двоичный код? Он содержит только нули и единицы, как они сами.",
    "Почему алкаши играют на Радмире? Они попутали своих соседок.",
    "Слышали о новом законе в Radmir RP? Теперь всем соседям обязательно нужно проводить еженедельные вечеринки - для поддержания соседских отношений.",

"Почему соседи главного героя в Radmir RP всегда такие любопытные? Потому что они следят за развитием сюжета лучше, чем сам главный герой.",

"Как называется соседка в Radmir RP, которая одалживает у всех сахар и муку? Профессиональный кондитер-заимодавец.",

"Что говорят две соседки в Radmir RP, когда случайно встречаются на лестничной площадке? О, привет! Ты тоже за почтой пришла?" "Нет, я просто соскучилась и решила выйти в коридор покурить."
]

@bot.message_handler(commands=['joke'])
def joke(message):
    random_joke = random.choice(jokes)
    bot.reply_to(message, random_joke)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Введите следующую информацию:")
    bot.send_message(message.chat.id, "Фамилия:")
    bot.register_next_step_handler(message, get_lastname)

def get_lastname(message):
    lastname = message.text
    bot.send_message(message.chat.id, "Имя:")
    bot.register_next_step_handler(message, get_firstname, lastname)

def get_firstname(message, lastname):
    firstname = message.text
    bot.send_message(message.chat.id, "Отчество:")
    bot.register_next_step_handler(message, get_middlename, lastname, firstname)

def get_middlename(message, lastname, firstname):
    middlename = message.text
    bot.send_message(message.chat.id, "Дата рождения (в формате ГГГГ-ММ-ДД):")
    bot.register_next_step_handler(message, save_data, lastname, firstname, middlename)

def save_data(message, lastname, firstname, middlename):
    birthday = message.text
    userid = message.chat.id
    username = message.chat.first_name

    con = sqlite3.connect('Tatarin.db')
    cur = con.cursor()
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS tgbot
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        userid integer,
        username TEXT,
        f TEXT,
        i TEXT,
        o TEXT,
        birthday TEXT)'''
    )
    cur.execute('''INSERT INTO tgbot (userid, username, f, i, o, birthday) VALUES (?, ?, ?, ?, ?, ?)''',
                (userid, username, lastname, firstname, middlename, birthday))


    cur.execute('''SELECT * FROM tgbot''')
    with open('TGBOTExport.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writter = csv.writer(csvfile)
        csv_writter.writerow(['id', 'userid', 'username', 'f', 'i', 'o', 'birthday'])
        csv_writter.writerows(cur)

    con.commit()
    con.close()

    bot.reply_to(message, "Ваши данные украдены - на вас оформлен кредит. Поздравляем!")

if __name__ == '__main__':
    bot.polling()
