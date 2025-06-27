import json
import os

import requests

from services.metadata.metadata_writer import MetadataWriter
from services.metadata.youtube_metadata_provider import YoutubeMetadataProvider

# metadata_writer = MetadataWriter()
# metadata_writer.write_metadata("/home/shivansh/Projects/PythonProjects/SongAPI/No Time To Die.mp3", {})
# metadata_writer.write_album_art("/home/shivansh/Projects/PythonProjects/SongAPI/No Time To Die.mp3", "/home/shivansh/Projects/PythonProjects/SongAPI/Billie_Eilish_-_No_Time_to_Die.png")

"https://i.scdn.co/image/ab67616d0000b273c4d00cac55ae1b4598c9bc90"

album_art = requests.get("https://i.scdn.co/image/ab67616d0000b273c4d00cac55ae1b4598c9bc90").content
with open("/home/shivansh/Projects/PythonProjects/SongAPI/album_art.jpg", "wb") as f:
    f.write(album_art)