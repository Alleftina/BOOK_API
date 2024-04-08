from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from database.connection import get_session
from main import app
from models.models import Author


@app.get("/authors")
def get_authors(session: Session = Depends(get_session)):
    # Получаем всех авторов из базы данных
    authors = session.query(Author).all()

    # Если список авторов пуст, возвращаем исключение HTTP 404 Not Found
    if not authors:
        raise HTTPException(status_code=404, detail="Список авторов пуст")

    # Возвращаем список имен авторов
    return {"authors": [author.name for author in authors]}


@app.post("/authors")
def create_author(name: str, session: Session = Depends(get_session)):
    # Проверяем, существует ли автор с таким именем
    existing_author = session.query(Author).filter_by(name=name).first()

    # Если автор уже существует, HTTP 409 Conflict
    if existing_author:
        raise HTTPException(status_code=409, detail="Автор с таким именем уже существует")

    # Создаем нового автора
    new_author = Author(name=name)

    # Добавляем автора в сессию и фиксируем изменения
    session.add(new_author)
    session.commit()

    # Возвращаем информацию о созданном авторе
    return {"message": "Автор успешно создан", "author": {"id": new_author.id, "name": new_author.name}}
