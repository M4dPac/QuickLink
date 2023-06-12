from clients.sqlite3_client import DatabaseManager

from config import HOST


def create_table():
    with DatabaseManager(creating=True):
        pass


def drop_table():
    with DatabaseManager() as client:
        client.drop_table()


def get_shorten_url(long_url: str) -> str:
    with DatabaseManager() as client:
        short_url = client.get_and_add_short_url(long_url)
    return short_url


def get_long_url(short_url: str) -> str:
    with DatabaseManager() as client:
        if not client.is_url_in_db(short_url):
            return HOST
        long_url = client.get_long_url(short_url)
    return long_url


if __name__ == "__main__":
    drop_table()
