import requests
import os
from dotenv import load_dotenv

load_dotenv()

CINEMA_API = os.getenv("CINEMA_API")

def get_showtimes(zipcode):

    url = (
        "https://api.api-cinema.com/v1/showtimes"
        f"?zip_code={zipcode}"
        "&country=US"
        "&include=movie,cinema"
    )

    headers = {
        "Authorization":
        f"Bearer {CINEMA_API}"
    }

    response = requests.get(
        url,
        headers=headers
    )

    return response.json()