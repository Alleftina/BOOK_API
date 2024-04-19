from sqlalchemy.orm import Session
from db.connection import get_session
from models.models import Author, Book


def fill_db(session: Session):
    # Создание авторов
    authors = [
        Author(name="George Orwell"),
        Author(name="Fyodor Dostoevsky"),
        Author(name="Jane Austen"),
    ]
    session.bulk_save_objects(authors)
    session.commit()

    # Создание книг
    books = [
        Book(title="1984", description="Nineteen Eighty-Four", authors=[authors[0]]),
        Book(title="Crime and Punishment", description="Преступление и наказание", authors=[authors[1]]),
        Book(title="Pride and Prejudice", description="Гордость и предубеждение", authors=[authors[2]]),
    ]
    session.bulk_save_objects(books)
    session.commit()



if __name__ == "__main__":
    session = get_session()
    fill_db(session)
