from sqlalchemy import text
from database import engine


def save_showtime(
    movie_title,
    theater_name,
    start_time
):

    with engine.connect() as connection:

        query = text("""
            INSERT INTO showtime
            (
                movie_title,
                theater_name,
                start_time
            )

            VALUES
            (
                :movie_title,
                :theater_name,
                :start_time
            )
        """)

        connection.execute(
            query,
            {
                "movie_title": movie_title,
                "theater_name": theater_name,
                "start_time": start_time
            }
        )

        connection.commit()