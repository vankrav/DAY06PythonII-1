import psycopg2

# Подключение к базе данных
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="postgres"
)

# Создание таблицы Books
cur = conn.cursor()
cur.execute('''
    CREATE TABLE Books (
        book_id SERIAL PRIMARY KEY,
        title VARCHAR(255),
        author VARCHAR(255),
        published INTEGER,
        date_added DATE,
        date_deleted DATE
    )
''')

# Создание таблицы Borrows
cur.execute('''
    CREATE TABLE Borrows (
        borrow_id SERIAL PRIMARY KEY,
        book_id INTEGER REFERENCES Books (book_id),
        date_start TIMESTAMP,
        date_end TIMESTAMP,
        user_id BIGINT
    )
''')

# Закрытие соединения с базой данных
cur.close()
conn.close()