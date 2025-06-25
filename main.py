from fastapi import FastAPI
from services.refactor import download_song
from pydantic import BaseModel
app = FastAPI()

class SongRequest(BaseModel):
    song_name: str

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/download_song")
async def say_hello(song: SongRequest):
    file_path = download_song(song.song_name)

    return {"message": f"You download {song.song_name}"}
