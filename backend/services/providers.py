import requests
import os
from dotenv import load_dotenv

load_dotenv()

TMDB_API = os.getenv("TMDB_API")

def get_watch_providers(movie_id):

    url = (
        f"https://api.themoviedb.org/3/movie/"
        f"{movie_id}/watch/providers"
        f"?api_key={TMDB_API}"
    )

    response = requests.get(url)

    return response.json()