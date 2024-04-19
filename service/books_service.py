from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.schemas import BookSchema
from models.models import Book
from service.authors_service import get_authors_by_names


def get_book_dict(session: Session, book_id: int) -> dict:
    book = session.query(Book).filter(Book.id == book_id).first()
    if not book:
        session.close()
        raise HTTPException(status_code=404, detail="Книга не найдена")

    data = {
        "id": book.id,
        "title": book.title,
        "description": book.description,
        "authors": book.authors
    }
    session.close()

    return data


def get_book_object(session: Session, book_id: int) -> Book:
    book = session.query(Book).filter(Book.id == book_id).first()
    if not book:
        session.close()
        raise HTTPException(status_code=404, detail="Книга не найдена")
    session.close()

    return book


def get_all_books(session: Session):
    # Получаем всех книг из базы данных
    books = session.query(Book).all()
    return books


def create_new_book(session: Session, title: str, description: str, authors: List[str]) -> dict:
    # Создаем новую книгу
    new_book = Book(title=title, description=description)

    # Проверяем, что для всех авторов существуют записи в базе данных
    if authors:
        existing_authors = get_authors_by_names(session, authors)
        new_book.authors = existing_authors

    # Добавляем книгу в сессию и фиксируем изменения
    session.add(new_book)
    session.flush()  # Подтверждаем добавление, но не закрываем сессию

    # Загружаем книгу обратно из базы данных, чтобы получить связанные авторы
    session.refresh(new_book)
    # Собираем информацию о книге для ответа
    book_data = {
        "id": new_book.id,
        "title": new_book.title,
        "description": new_book.description,
        "authors": [{"id": author.id, "name": author.name} for author in new_book.authors]
    }
    session.commit()
    session.close()

    return book_data


def update_book(session: Session, book_id: int, title: str = None, description: str = None,
                authors: List[str] | None = None) -> Book:
    # Получаем книгу по ее идентификатору
    book = session.query(Book).filter(Book.id == book_id).first()

    # Если книга не найдена, исключение HTTP 404 Not Found
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    # Обновляем название книги, если предоставлено новое значение
    if title is not None:
        book.title = title

    # Обновляем описание книги, если предоставлено новое значение
    if description is not None:
        book.description = description


    # Фиксируем изменения в базе данных
    session.commit()

    # Обновляем объект книги в сессии
    session.refresh(book)

    return book