from pydantic import BaseModel


class Author(BaseModel):
    id: int
    name: str

class Book(BaseModel):
    id: int
    title: str
    description: str
    authors: str
