from sqlalchemy import text
from database import engine


def save_movie(
    tmdb_id,
    title,
    release_date,
    rating,
    overview
):

    with engine.connect() as connection:

        query = text("""
            INSERT INTO movie
            (
                tmdb_id,
                title,
                release_date,
                rating,
                overview
            )

            VALUES
            (
                :tmdb_id,
                :title,
                :release_date,
                :rating,
                :overview
            )
        """)

        connection.execute(
            query,
            {
                "tmdb_id": tmdb_id,
                "title": title,
                "release_date": release_date,
                "rating": rating,
                "overview": overview
            }
        )

        connection.commit()