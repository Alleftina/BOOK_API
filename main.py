import os
import sys
from fastapi import FastAPI
from pydantic_settings import BaseSettings

from endpoints.authors import router as router_authors
from endpoints.books import router as router_books



app = FastAPI(
    title="Book API TEST"
)

app.include_router(router_authors)
app.include_router(router_books)


