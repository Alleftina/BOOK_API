from typing import List, Optional
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy import select
from sqlalchemy.orm.session import Session
from db.connection import get_session
from models.models import Book, Author
from models.schemas import BookSchema, AuthorSchema, AuthorName
from service.books_service import create_new_book, get_book_dict, update_book, get_all_books, get_book_object

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


@router.get("", description="Получение списка всех книг.", response_model=List[BookSchema])
def get_books(session: Session = Depends(get_session)):
    books = get_all_books(session)
    if not books:
        raise HTTPException(status_code=404, detail="Список книг пуст")
    return books


@router.post("", description="Создание новой книги.", response_model=BookSchema)
def create_book(title: str, description: str, authors:  Optional[AuthorName], session: Session = Depends(get_session)):
    new_book = create_new_book(session, title, description, authors.names)

    return new_book


@router.get("/{book_id}", description="Получение книги по идентификатору.", response_model=BookSchema)
def get_book_by_id(book_id: int, session: Session = Depends(get_session)):
    # Получаем книгу по ее идентификатору
    book = get_book_dict(session, book_id)
    # Если книга не найдена
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    # Если книга найдена, возвращаем информацию о ней
    return book


@router.put("/{book_id}", description="Обновление информации о книге.", response_model=BookSchema)
def update_book_by_id(book_id: int, title: str = None, description: str = None, authors: Optional[AuthorName] = [],
                      session: Session = Depends(get_session)):
    book = update_book(session, book_id, title, description, authors)

    return book


@router.delete("/{book_id}", description="Удаление книги по идентификатору.", response_model=dict)
def delete_book_by_id(book_id: int, session: Session = Depends(get_session)):
    # Получаем книгу по её идентификатору
    book = get_book_object(session, book_id)
    # Если книга не найдена, HTTP 404 Not Found
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    # Удаляем книгу
    session.delete(book)
    session.commit()
    return {"message": "Книга успешно удалена"}
