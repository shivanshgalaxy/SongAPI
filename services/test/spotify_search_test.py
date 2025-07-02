import os

from dotenv import load_dotenv

from services.metadata.metadata_writer import MetadataWriter
from services.metadata.song_id import SongIDService
from services.metadata.spotify_metadata_provider import SpotifyMetadataProvider
from services.metadata.youtube_metadata_provider import YoutubeMetadataProvider
from services.metadata_manger import MetadataManager
from services.spotify_auth import get_token

load_dotenv()
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
token = get_token(client_id, client_secret)

# https://open.spotify.com/track/3zL0LAsSh3dTO73dSOKWkr?si=8bbf02d0b0c346ea

youtube = YoutubeMetadataProvider()
spotify = SpotifyMetadataProvider(token)
writer = MetadataWriter()
manager = MetadataManager([spotify, youtube], writer)
# metadata = manager.get_metadata("https://music.youtube.com/watch?v=8WuVWqyGPcs&si=OuAeaw6-il7Grllf")

manager.write_album_art("/home/sh/Projects/PycharmProjects/SongDownloader/Sweden.mp3", "/home/sh/Projects/PycharmProjects/SongDownloader/No Time To Die_cover.jpg")

# spotify_id = SongIDService(token)
# print(spotify_id.extract_spotify_track_id("https://open.spotify.com/track/4NsPgRYUdHu2Q5JRNgXYU5"))

from mutagen.id3 import ID3, ID3NoHeaderError

mp3_path = "/home/sh/Projects/PycharmProjects/SongDownloader/Sweden.mp3"

try:
    tags = ID3(mp3_path)
    print("ID3 version:", tags.version)
    has_cover = any(key.startswith("APIC") for key in tags.keys())
    print("Has cover art:", has_cover)
except ID3NoHeaderError:
    print("No ID3 tag found in the file.")