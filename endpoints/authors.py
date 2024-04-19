from typing import List
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from db.connection import get_session
from models.models import Author
from models.schemas import AuthorSchema
from service.authors_service import get_all_authors, create_new_author

router = APIRouter(
    prefix="/authors",
    tags=["Authors"]
)


@router.get("", description="Получение списка всех авторов.", response_model=List[AuthorSchema])
def get_authors(session: Session = Depends(get_session)):
    authors = get_all_authors(session)
    if not authors:
        raise HTTPException(status_code=404, detail="Список авторов пуст")
    return authors


@router.post("", description="Создание нового автора.", response_model=AuthorSchema)
def create_author(name: str, session: Session = Depends(get_session)):
    new_author = create_new_author(session, name)
    return new_author
