import psycopg2
from .models import Book
import pandas as pd

class DatabaseConnector:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
    def connect(self):
        return psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )
    def add(self, book):
        conn = self.connect()
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO "Books" (title, author, published, date_added, date_deleted)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING book_id;
            """, (book.title, book.author, book.published, book.date_added, book.date_deleted))
            book_id = cur.fetchone()[0]
            conn.commit()
            return book_id
    def delete(self, book_id):
        conn = self.connect()
        with conn.cursor() as cur:
            # Проверяем, что книга не находится в аренде
            cur.execute("""
                SELECT COUNT(*) FROM "Borrows"
                WHERE book_id = %s AND date_end IS NULL;
            """, (book_id,))
            if cur.fetchone()[0] > 0:
                return False

            # Обновляем дату удаления книги
            cur.execute("""
                UPDATE "Books" SET date_deleted = NOW()
                WHERE book_id = %s;
            """, (book_id,))
            conn.commit()
            return True
    def list_books(self):
        conn = self.connect()
        with conn.cursor() as cur:
            cur.execute("""SELECT * FROM "Books" ;""")
            books = cur.fetchall()
            return books
    def get_book_by_id(self, id):
        conn = self.connect()
        with conn.cursor() as cur:
            cur.execute("""
                SELECT title, author, published FROM "Books"
                WHERE book_id = %s AND date_deleted IS NULL;
            """, (id,))
            result = cur.fetchone()
            return result if result else None
    def get_book_borrows(self, book_id):
        conn = self.connect()
        df = pd.read_sql(f"""SELECT borrow_id, book_id, date_start, date_end FROM "Borrows" WHERE book_id = {book_id};""", conn)
        return df
        # with conn.cursor() as cur:
        #     cur.execute("""
        #         SELECT borrow_id, book_id, date_start, date_end FROM "Borrows"
        #         WHERE book_id = %s;
        #     """, (book_id,))
        #     result = cur.fetchall()
        #     return result if result else None
    def get_book(self, title, author):
        conn = self.connect()
        with conn.cursor() as cur:
            cur.execute("""
                SELECT book_id FROM "Books"
                WHERE LOWER(title) = LOWER(%s) AND LOWER(author) = LOWER(%s)
                    AND date_deleted IS NULL;
            """, (title, author))
            result = cur.fetchone()
            return result[0] if result else None
    def borrow(self, book_id, user_id):
        conn = self.connect()
        with conn.cursor() as cur:
            # Проверяем, что книга не находится в аренде
            cur.execute("""
                SELECT COUNT(*) FROM "Borrows"
                WHERE book_id = %s AND date_end IS NULL;
            """, (book_id,))
            if cur.fetchone()[0] > 0:
                return False

            # Проверяем, что пользователь не берет больше одной книги в аренду
            cur.execute("""
                SELECT COUNT(*) FROM "Borrows"
                WHERE user_id = %s AND date_end IS NULL;
            """, (user_id,))
            if cur.fetchone()[0] > 0:
                return False

            # Добавляем запись об аренде книги
            cur.execute("""
                INSERT INTO "Borrows" (book_id, date_start, user_id)
                VALUES (%s, NOW(), %s)
                RETURNING borrow_id;
            """, (book_id, user_id))
            borrow_id = cur.fetchone()[0]
            conn.commit()
            return borrow_id
    def get_borrow(self, user_id):
        conn = self.connect()
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    SELECT borrow_id FROM "Borrows"
                    WHERE user_id = %s
                    AND date_end IS NULL;
                """, (user_id,))
                borrow_id = cur.fetchone()
                if borrow_id is None:
                    return None
                else:
                    return borrow_id[0]
            except psycopg2.Error as e:
                print(f"Error: Could not get borrow from database\n{e}")
                return None
    def retrieve(self, borrow_id, date_returned):
        conn = self.connect()
        with conn.cursor() as cur:
            try:
                cur.execute(
                    """
                    UPDATE "Borrows" SET date_end = %s WHERE borrow_id = %s;
                    """, (date_returned, borrow_id))
                conn.commit()
                cur.execute(
                    """
                    SELECT book_id FROM "Borrows"
                    WHERE borrow_id = %s;
                    """,(borrow_id,))

                result = cur.fetchone()

                return result if result else None
            except psycopg2.Error as e:
                print(f"Error: Couldhjhh not get borrow from database\n{e}")
                return None


