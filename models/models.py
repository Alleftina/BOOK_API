from sqlalchemy import MetaData, String, TIMESTAMP, ForeignKey, Table, Column, Integer
from database.connection import Base
from sqlalchemy.orm import relationship

metadata = MetaData()

# Таблица для связи книг и авторов (многие ко многим)
book_author_association = Table(
    'book_author_association',
    Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id')),
    Column('author_id', Integer, ForeignKey('authors.id'))
)


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    # Связь с книгами: многие ко многим
    books = relationship("Book", secondary=book_author_association, back_populates="authors")


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)

    # Связь с авторами: многие ко многим
    authors = relationship("Author", secondary=book_author_association, back_populates="books")
