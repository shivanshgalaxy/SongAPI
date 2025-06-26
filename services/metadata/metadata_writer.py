from mutagen.mp3 import EasyMP3, MP3
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC

class MetadataWriter:
    def write_text(self, filepath: str, metadata: dict) -> None:
        audio = EasyMP3(filepath)
        audio.delete()
        for key, value in metadata.items():
            if key in EasyID3.valid_keys.keys():
                audio[key] = value
        audio.save()

    def add_album_art(self, audio_filepath: str, image_filepath: str):
        audio = MP3(audio_filepath)

        with open(image_filepath, 'rb') as img:
            audio.tags.add(
                APIC(
                    encoding=3,  # UTF-8
                    mime='image/jpeg',  # or 'image/png'
                    type=3,  # 3 is for cover (front)
                    desc='Cover',
                    data=img.read()
                )
            )

        audio.save()


writer = MetadataWriter()
writer.write_text("/home/sh/Projects/PycharmProjects/SongDownloader/Faded.mp3", {"artist" : "Alan Walker", "title": "Faded"})
writer.add_album_art("/home/sh/Projects/PycharmProjects/SongDownloader/Faded.mp3",
                     "/home/sh/Projects/PycharmProjects/SongDownloader/faded.jpg")
