from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создание подключения к базе данных
engine = create_engine('postgresql://postgres:171278@localhost/postgres')
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Описание модели Book
class Book(Base):
    __tablename__ = 'Books'

    book_id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    published = Column(Integer)
    date_added = Column(Date)
    date_deleted = Column(Date)

# Описание модели Borrow
class Borrow(Base):
    __tablename__ = 'Borrows'

    borrow_id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('Books.book_id'))
    date_start = Column(DateTime)
    date_end = Column(DateTime)
    user_id = Column(Integer)

# Создание таблиц в базе данных
Base.metadata.create_all(engine)

# Использование модели Book
session = Session()
# book = Book(title='The Lord of the Rings', author='J.R.R. Tolkien', published=1954, date_added='2023-04-14', date_deleted=None)
# session.add(book)
# session.commit()
#
# # Использование модели Borrow
# borrow = Borrow(book_id=1, date_start='2023-04-14 10:00:00', date_end=None, user_id=123456)
# session.add(borrow)
# session.commit()

# Закрытие соединения с базой данных
session.close()
engine.dispose()
