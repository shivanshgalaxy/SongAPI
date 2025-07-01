from mutagen.mp3 import EasyMP3, MP3
from mutagen.easyid3 import EasyID3
from mutagen.id3 import APIC

class MetadataWriter:
    @staticmethod
    def write_metadata(filepath: str, metadata: dict) -> None:
        audio = EasyMP3(filepath)
        audio.delete()
        for key, value in metadata.items():
            if key in EasyID3.valid_keys.keys():
                audio[key] = value
        audio.save(v2_version=3)

    @staticmethod
    def write_album_art(filepath: str, image_path: str) -> None:
        audio = MP3(filepath)
        print(image_path)
        with open(image_path, 'rb') as img:
            audio.tags.add(
                APIC(
                    encoding=3,  # UTF-8
                    mime='image/jpeg',  # or 'image/png'
                    type=3,  # 3 is for cover (front)
                    desc='Cover',
                    data=img.read()
                )
            )
        audio.save(v2_version=3)
