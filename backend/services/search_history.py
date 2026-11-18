from sqlalchemy import text
from database import engine


def save_search(search_type, search_value):

    print("Saving search:", search_type, search_value)

    with engine.connect() as connection:

        query = text("""

            INSERT INTO search_history
            (
                search_type,
                search_value
            )

            VALUES
            (
                :search_type,
                :search_value
            )

        """)

        connection.execute(
            query,
            {
                "search_type": search_type,
                "search_value": search_value
            }
        )

        connection.commit()


def get_recent_searches():

    with engine.connect() as connection:

        query = text("""
            SELECT search_value
            FROM search_history
            ORDER BY history_id DESC
            LIMIT 5
        """)

        results = connection.execute(query)

        return results.fetchall()
