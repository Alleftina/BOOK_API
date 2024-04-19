from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.models import Author


def get_all_authors(session: Session):
    # Получаем всех авторов из базы данных
    authors = session.query(Author).all()
    return authors


def get_authors_by_names(session: Session, authors: List[str]) -> List[Author]:
    existing_authors = []
    for author_name in authors:
        existing_author = session.query(Author).filter_by(name=author_name).first()
        if not existing_author:
            raise HTTPException(status_code=400, detail=f"Автор '{author_name}' не найден")
        existing_authors.append(existing_author)
    session.close()
    return existing_authors


def create_new_author(session: Session, name: str) -> dict:
    existing_author = session.query(Author).filter_by(name=name).first()
    if existing_author:
        raise HTTPException(status_code=409, detail="Автор с таким именем уже существует")

    new_author = Author(name=name)
    session.add(new_author)
    session.commit()
    data = {
        "id": new_author.id,
        "name": new_author.name
    }
    session.close()

    return data

