from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import re
from services.tmdb_service import search_movie
from services.search_history import save_search, get_recent_searches
from services.movies import save_movie
from services.providers import get_watch_providers
from services.cinema_service import get_cinemas
from services.theater import save_theater
from services.showtime_service import get_showtimes
from services.database import save_showtime


app = FastAPI()

app.mount(
    "/styles",
    StaticFiles(directory="styles"),
    name="styles"
)

template = Jinja2Templates(directory="template")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    searches = get_recent_searches()

    return template.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "searches": searches
        }
    )

@app.get("/providers")
def providers(movie_id: int):
    
    return get_watch_providers(movie_id)

@app.get("/theater-search")
def theater_search(request: Request):

    return template.TemplateResponse(
        request=request,
        name="theater_search.html"
    )

@app.get("/movie-search-page", response_class=HTMLResponse)
def movie_search_page(request: Request, title: str):

    data = search_movie(title)
    
    if len(data["results"]) == 0:

        return template.TemplateResponse(
            request=request,
            name="search_result.html",
            context={
                "movie": None,
                "providers": []
            }
        )

    movie = data["results"][0]
    providers = get_watch_providers(movie["id"])

    provider_list = []

    try:

        us_providers = providers["results"]["US"]["flatrate"]

        for provider in us_providers:

            provider_list.append(
                provider["provider_name"]
            )

    except KeyError:

        provider_list.append(
            "No streaming providers found"
        )

    save_search(
    "movie",
    title
    )

    if len(data["results"]) == 0:

        return {
            "message": "No movie found"
        }


    save_movie(
        movie["id"],
        movie["title"],
        movie["release_date"],
        movie["vote_average"],
        movie["overview"]
    )

    return template.TemplateResponse(
        request=request,
        name="search_result.html",
        context={
            "movie": movie,
            "providers": provider_list,
        }
    )

@app.get("/theater-results")
def theater_results(
    request: Request,
    zipcode: str
):

    if not re.match(
        r'^\d{5}$',
        zipcode
    ):

        return {
            "message":
            "Please enter a valid ZIP code."
        }

    results = get_cinemas(zipcode)

    theaters = results["data"]

    for theater in theaters:

        save_theater(
            theater["name"],
            theater.get("address"),
            theater.get("city"),
            theater.get("postalCode")
        )

    return template.TemplateResponse(
        request=request,
        name="theater_results.html",
        context={
            "theaters": theaters
        }
    )

@app.get("/showtimes")
def showtimes(
    request: Request,
    zipcode: str
):

    results = get_showtimes(zipcode)

    print(results)

    showtimes = results["data"]

    for showtime in showtimes:

        save_showtime(
            showtime["movie"]["title"],
            showtime["cinema"]["name"],
            showtime["startsAt"]
        )

    return template.TemplateResponse(
        request=request,
        name="showtimes.html",
        context={
            "showtimes": showtimes
        }
    )