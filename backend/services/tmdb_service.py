import requests
from dotenv import load_dotenv
import os

load_dotenv()

TMDB_API = os.getenv("TMDB_API")

def search_movie(title):

    url = (
        f"https://api.themoviedb.org/3/search/movie"
        f"?api_key={TMDB_API}"
        f"&query={title}"
    )

    response = requests.get(url)

    return response.json()