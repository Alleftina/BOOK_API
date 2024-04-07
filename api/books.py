from main import app

@app.get("/books")
def hello():
    return "Hello wrold"


@app.post("/books")
def hello():
    return "Hello wrold"


@app.get("/books/{book_id}")
def hello(book_id: int):
    return f"Hello {book_id}"


@app.put("/books/{book_id}")
def hello(book_id: int):
    return "Hello wrold"


@app.delete("/books/{book_id}")
def hello(book_id: int):
    return "Hello wrold"

