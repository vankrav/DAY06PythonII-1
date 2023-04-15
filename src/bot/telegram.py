import telebot
from datetime import date

#@BibibibibloBot

from database.dbapi import DatabaseConnector
from database.models import Book

db = DatabaseConnector("localhost", "postgres", "postgres", "postgres")
# Создаем телеграм-бота
bot = telebot.TeleBot("5803716884:AAFf1NYV8q94O5Zk60qPQu9hxIDHgMqPAHY")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    response = "Привет! Я бот для управления библиотекой.\n\n"
    response += "Доступные команды:\n"
    response += "/add - добавить книгу в базу данных\n"
    response += "/delete - удалить книгу из базы данных\n"
    response += "/list - получить список всех книг\n"
    response += "/find - найти книгу по названию, автору и году издания\n"
    response += "/borrow - взять книгу из библиотеки\n"
    response += "/retrieve - вернуть книгу в библиотеку\n"
    response += "/stats - получить статистику по книге\n"
    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['add'])
def add_book(message):
    # Запрос на ввод названия книги
    bot.send_message(message.chat.id, "Введите название книги:")
    bot.register_next_step_handler(message, add_book_author)
def add_book_author(message):
    # Сохраняем название книги в переменную и запрашиваем автора
    book_title = message.text
    bot.send_message(message.chat.id, "Введите автора:")
    bot.register_next_step_handler(message, add_book_year, book_title)
def add_book_year(message, book_title):
    # Сохраняем автора в переменную и запрашиваем год издания
    book_author = message.text
    bot.send_message(message.chat.id, "Введите год издания:")
    bot.register_next_step_handler(message, add_book_to_database, book_title, book_author)
def add_book_to_database(message, book_title, book_author):
    # Сохраняем год издания в переменную и добавляем книгу в БД
    try:
        book_year = int(message.text)
        book = Book(title=book_title, author=book_author, published=book_year, date_added=date.today(), date_deleted=None)
        book_id = db.add(book)
        bot.send_message(message.chat.id, f"Книга добавлена (id {book_id})")
    except ValueError:
        bot.send_message(message.chat.id, "Некорректный ввод года издания")
    except:
        bot.send_message(message.chat.id, "Ошибка при добавлении книги")


@bot.message_handler(commands=['delete'])

def delete_book(message):
    # Запрос на ввод названия книги
    bot.send_message(message.chat.id, "Введите название книги:")
    bot.register_next_step_handler(message, delete_book_author)
def delete_book_author(message):
    # Сохраняем название книги в переменную и запрашиваем автора
    book_title = message.text
    bot.send_message(message.chat.id, "Введите автора:")
    bot.register_next_step_handler(message, delete_book_year, book_title)
def delete_book_year(message, book_title):
    # Сохраняем автора в переменную и запрашиваем год издания
    book_author = message.text
    bot.send_message(message.chat.id, "Введите год издания:")
    bot.register_next_step_handler(message, delete_book_find, book_title, book_author)
def delete_book_find(message, book_title, book_author):
    try:
        book_year = int(message.text)
        print(book_title, book_author)
        book_id = db.get_book(book_title, book_author)
        if book_id:
            bot.send_message(message.chat.id, f"Найдена книга: {book_title} {book_author} {book_year} Удаляем?")
            bot.send_message(message.chat.id, "Да/Нет")
        else:
            bot.send_message(message.chat.id, f"Книга не найдена")
    except ValueError:
        bot.send_message(message.chat.id, "Некорректный ввод года издания")
    except:
        bot.send_message(message.chat.id, "Ошибка при поиске книги")
    bot.register_next_step_handler(message, delete_book_from_database, book_title, book_author, book_id)
def delete_book_from_database(message, book_title, book_author, book_id):
       if message.text.lower() == "да":
          if db.delete(book_id):
              bot.send_message(message.chat.id, "Книга удалена")
          else:
              bot.send_message(message.chat.id, "Невозможно удалить книгу")

@bot.message_handler(commands=['find'])
def find_book(message):
    # Запрос на ввод названия книги
    bot.send_message(message.chat.id, "Введите название книги:")
    bot.register_next_step_handler(message, find_book_author)
def find_book_author(message):
    # Сохраняем название книги в переменную и запрашиваем автора
    book_title = message.text
    bot.send_message(message.chat.id, "Введите автора:")
    bot.register_next_step_handler(message, find_book_year, book_title)
def find_book_year(message, book_title):
    # Сохраняем автора в переменную и запрашиваем год издания
    book_author = message.text
    bot.send_message(message.chat.id, "Введите год издания:")
    bot.register_next_step_handler(message, find_book_result, book_title, book_author)
def find_book_result(message, book_title, book_author):
    try:
        book_year = int(message.text)
        print(book_title, book_author)
        book_id = db.get_book(book_title, book_author)
        if book_id:
            bot.send_message(message.chat.id, f"Найдена книга: {book_title} {book_author} {book_year}")
        else:
            bot.send_message(message.chat.id, f"Такой книги у нас нет")
    except ValueError:
        bot.send_message(message.chat.id, "Некорректный ввод года издания")
    except:
        bot.send_message(message.chat.id, "Ошибка при поиске книги")

@bot.message_handler(commands=['borrow'])

def borrow_book(message):
    # Запрос на ввод названия книги
    bot.send_message(message.chat.id, "Введите название книги:")
    bot.register_next_step_handler(message, borrow_book_author)
def borrow_book_author(message):
    # Сохраняем название книги в переменную и запрашиваем автора
    book_title = message.text
    bot.send_message(message.chat.id, "Введите автора:")
    bot.register_next_step_handler(message, borrow_book_year, book_title)
def borrow_book_year(message, book_title):
    # Сохраняем автора в переменную и запрашиваем год издания
    book_author = message.text
    bot.send_message(message.chat.id, "Введите год издания:")
    bot.register_next_step_handler(message, borrow_book_find, book_title, book_author)
def borrow_book_find(message, book_title, book_author):
    try:
        book_year = int(message.text)
        print(book_title, book_author)
        book_id = db.get_book(book_title, book_author)
        if book_id:
            bot.send_message(message.chat.id, f"Найдена книга: {book_title} {book_author} {book_year} Берем?")
            bot.send_message(message.chat.id, "Да/Нет")
        else:
            bot.send_message(message.chat.id, f"Книга не найдена")
    except ValueError:
        bot.send_message(message.chat.id, "Некорректный ввод года издания")
    except:
        bot.send_message(message.chat.id, "Ошибка при поиске книги")
    bot.register_next_step_handler(message, borrow_book_from_database, book_title, book_author, book_id)
def borrow_book_from_database(message, book_title, book_author, book_id):
       if message.text.lower() == "да":
          if db.borrow(book_id, message.chat.id):
              bot.send_message(message.chat.id, "Вы взяли книгу")
          else:
              bot.send_message(message.chat.id, "Книгу сейчас невозможно взять")

@bot.message_handler(commands=['retrieve'])
def retrieve_book(message):
    borrow_id = db.get_borrow(message.chat.id)
    book_id = db.retrieve(borrow_id, date.today())
    result = db.get_book_by_id(book_id)

    bot.send_message(message.chat.id, f"Вы вернули книгу {result[0]} {result[1]} {result[2]}")

@bot.message_handler(commands=['list'])
def list(message):
    response = db.list_books()
    s = ""
    for i in response:
        s+= f"{i[1]}, {i[2]}, {i[3]}{' (удалена)' if  i[5] != None else ''};\n"

    bot.send_message(message.chat.id, s)



bot.polling()