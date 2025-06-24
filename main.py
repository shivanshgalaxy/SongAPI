from fastapi import FastAPI
from services.refactor import download_song

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/download_song/{song_name}")
async def say_hello(song_name: str):
    file_path = download_song(song_name)

    return {"message": f"You download {song_name}"}