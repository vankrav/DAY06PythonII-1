from flask import Flask, send_file
import pandas as pd
from dbapi import DatabaseConnector

app = Flask(__name__)

# Папка, в которой будут временно храниться файлы со статистикой
DOWNLOAD_FOLDER = '/path/to/download/folder'
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER


@app.route('/download/<int:book_id>')
def download_stats(book_id):
    # Получаем данные о заимах книги из БД
    db = DatabaseConnector()
    borrows = db.get_book_borrows(book_id)

    if not borrows:
        return 'Статистика использования книги не найдена'

    # Создаем DataFrame из полученных данных
    df = pd.DataFrame(borrows, columns=['borrow_id', 'book_id', 'user_id', 'date_start', 'date_end'])

    # Удаляем колонку user_id, чтобы не передавать личные данные пользователя
    df.drop(columns=['user_id'], inplace=True)

    # Генерируем имя файла для сохранения
    filename = f'stats_book_{book_id}.xlsx'
    filepath = f'{DOWNLOAD_FOLDER}/{filename}'

    # Сохраняем DataFrame в эксель-файле
    df.to_excel(filepath, index=False)

    # Отправляем файл пользователю
    return send_file(filepath, attachment_filename=filename, as_attachment=True)


if __name__ == '__main__':
    app.run()
