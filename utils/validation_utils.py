import validators
import re

def is_valid_url(url: str) -> bool:
    return validators.url(url)

def sanitize_filename(filename: str) -> str:
    # Remove special characters from the filename
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def extract_spotify_id(url: str) -> str:
    """
    Extracts the ID from a Spotify URL. Supports track, playlist, album, artist.
    """
    pattern = r"spotify\.com\/(?:track|album|playlist|artist)\/([a-zA-Z0-9]+)"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    raise ValueError("Invalid Spotify URL: unable to extract ID")
