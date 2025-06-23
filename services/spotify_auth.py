import base64
from requests import post
import os
import json
import time

TOKEN_FILE = "token.json"
TOKEN_URL = "https://accounts.spotify.com/api/token"
CONTENT_TYPE = "application/x-www-form-urlencoded"


def save_token(token: str, expires_in: int) -> None:
    data = {
        "access_token": token,
        "expires_at": time.time() + expires_in - 60
    }
    with open(TOKEN_FILE, "w") as f:
        json.dump(data, f)

def load_token() -> str | None:
    if not os.path.exists(TOKEN_FILE):
        return None
    with open(TOKEN_FILE, "r") as f:
        data = json.load(f)
    if data["expires_at"] > time.time():
        return data["access_token"]
    return None

def get_token(client_id: str, client_secret: str) -> str:
    token = load_token()
    if token:
        return token

    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": CONTENT_TYPE
    }
    data = { "grant_type": "client_credentials" }
    result = post(TOKEN_URL, headers=headers, data=data)
    try:
        result.raise_for_status()
    except:
        raise ValueError(f"Failed to retrieve access token: {result.status_code} {result.text}")
    json_result = result.json()
    token = json_result.get("access_token")
    if not token:
        raise ValueError("Failed to retrieve access token from Spotify API.")
    save_token(token, json_result.get("expires_in", 3600))
    return token