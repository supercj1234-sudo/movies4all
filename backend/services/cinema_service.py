import requests
import os
from dotenv import load_dotenv

load_dotenv()
CINEMA_API = os.getenv("CINEMA_API")


def get_cinemas(zipcode):

    url = (
        "https://api.api-cinema.com/v1/cinemas"
        f"?zip_code={zipcode}"
        "&country=US"
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