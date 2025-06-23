import os
from dotenv import load_dotenv
from spotify_auth import get_token
from requests import get
import json

load_dotenv()
def main():
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise EnvironmentError("Please set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET in your .env file.")
        return

    token = get_token(client_id, client_secret)
    headers = {
        "Authorization": f"Bearer {token}"
    }



main()