from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm.session import Session
from database.connection import get_session
from main import app
from models.models import Book, Author


@app.get("/books")
def get_books(session: Session = Depends(get_session)):
    query = session.query(Book.title, Author.name).join(Book.authors)
    return query.all()


@app.post("/books")
def create_book(title: str, description: str, authors: List[str], session: Session = Depends(get_session)):
    # Проверяем, что для всех авторов существуют записи в базе данных
    for author_name in authors:
        existing_author = session.query(Author).filter_by(name=author_name).first()
        if not existing_author:
            raise HTTPException(status_code=400, detail=f"Автор '{author_name}' не найден")

    # Создаем новую книгу
    new_book = Book(title=title, description=description)

    # Добавляем книгу в сессию и фиксируем изменения
    session.add(new_book)
    session.commit()

    # Добавляем книгу каждому автору
    for author_name in authors:
        existing_author = session.query(Author).filter_by(name=author_name).first()
        new_book.authors.append(existing_author)

    # Фиксируем изменения после добавления книги каждому автору
    session.commit()

    # Закрываем сессию
    session.close()


@app.get("/books/{book_id}")
def get_book_by_id(book_id: int, session: Session = Depends(get_session)):
    # Получаем книгу по ее идентификатору
    book = session.query(Book).filter(Book.id == book_id).first()

    # Если книга не найдена, вызываем исключение HTTPException с кодом 404
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    # Если книга найдена, возвращаем информацию о ней
    return {
        "title": book.title,
        "description": book.description,
        "authors": [author.name for author in book.authors]
    }


@app.put("/books/{book_id}")
def update_book_by_id(book_id: int, title: str = None, description: str = None, authors: List[str] | None = None,
                      session: Session = Depends(get_session)):
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

    # Обновляем авторов книги
    if authors:
        # Проверяем, что для всех авторов существуют записи в базе данных
        for author_name in authors:
            existing_author = session.query(Author).filter_by(name=author_name).first()
            if not existing_author:
                raise HTTPException(status_code=400, detail=f"Автор '{author_name}' не найден")

        # Очищаем текущих авторов книги
        book.authors.clear()

        # Добавляем новых авторов книги
        for author_name in authors:
            existing_author = session.query(Author).filter_by(name=author_name).first()
            book.authors.append(existing_author)

    # Фиксируем изменения в базе данных
    session.commit()

    # Возвращаем обновленную информацию о книге
    return {"message": "Книга успешно обновлена",
            "book": {"id": book.id, "title": book.title, "description": book.description,
                     "authors": [author.name for author in book.authors]}}


@app.delete("/books/{book_id}")
def delete_book(book_id: int, session: Session = Depends(get_session)):
    # Получаем книгу по её идентификатору
    book = session.query(Book).filter(Book.id == book_id).first()

    # Если книга не найдена, HTTP 404 Not Found
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    # Удаляем книгу
    session.delete(book)
    session.commit()

    return {"message": "Книга успешно удалена"}

