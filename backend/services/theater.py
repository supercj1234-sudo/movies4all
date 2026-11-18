from sqlalchemy import text
from database import engine


def save_theater(
    name,
    address,
    city,
    zipcode
):

    with engine.connect() as connection:

        query = text("""
            INSERT INTO theater
            (
                name,
                address,
                city,
                zipcode
            )

            VALUES
            (
                :name,
                :address,
                :city,
                :zipcode
            )
        """)

        connection.execute(
            query,
            {
                "name": name,
                "address": address,
                "city": city,
                "zipcode": zipcode
            }
        )

        connection.commit()