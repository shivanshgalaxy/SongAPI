import validators
import re

def is_valid_url(url: str) -> bool:
    return validators.url(url)

def sanitize_filename(filename: str) -> str:
    # Remove special characters from the filename
    return re.sub(r'[<>:"/\\|?*]', '', filename)