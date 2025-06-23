from fastapi import FastAPI

app = FastAPI()

items = []

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
@app.post("/items")
def create_item(item: str):
    items.append(item)
    return items
