from typing import List, Optional

from pydantic import BaseModel



class AuthorName(BaseModel):
    names: List[str]


class AuthorSchema(BaseModel):
    id: int
    name: str


class BookSchema(BaseModel):
    id: int
    title: str
    description: str
    authors: Optional[List[AuthorSchema]]

