from main import app



@app.get("/authors")
def hello():
    return "Hello wrold"


@app.post("/authors")
def hello():
    return "Hello wrold"
