import os
from dotenv import load_dotenv
from spotify_auth import get_token

load_dotenv()
def main():
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    token = get_token(client_id, client_secret)
    
    pass

if __name__ == "__refactor__":
    main()