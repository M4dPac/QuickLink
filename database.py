import sqlite3
from generate import generate_random_string


class DatabaseManager:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute(''' DROP TABLE IF EXISTS links ''')
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_url TEXT NOT NULL,
            long_url TEXT NOT NULL
            )
            ''')

    def add_short_url(self, long_url: str) -> str:
        short_url = generate_random_string()
        self.cursor.execute(f'''
        INSERT INTO links (short_url, long_url)
        VALUES ('{short_url}', '{long_url}')
        ''')
        self.conn.commit()
        return short_url

    def get_short_url(self, long_url: str) -> str:
        self.cursor.execute(f'''
        SELECT short_url FROM links WHERE long_url = '{long_url}'
        ''')
        return self.cursor.fetchone()[0]

    def get_long_url(self, short_url: str) -> str:
        self.cursor.execute(f'''
        SELECT long_url FROM links WHERE short_url = '{short_url}'
        ''')
        return self.cursor.fetchone()[0]

    def delete_short_url(self, short_url: str) -> None:
        self.cursor.execute(f'''
        DELETE FROM links WHERE short_url = '{short_url}'
        ''')


if __name__ == "__main__":
    db = DatabaseManager()
    long_link = "https://www.google.com"
    short_link = db.add_short_url(long_link)

    current_link = db.get_short_url(long_link)
    assert current_link == short_link, f"Wrong short link, curent link: {current_link}, expected link: {short_link}"

    current_link = db.get_long_url(short_link)
    assert current_link == long_link, f"Wrong long link, curent link: {current_link}, expected link: {long_link}"
    db.delete_short_url(short_link)
    print(db.cursor.execute(''' SELECT * FROM links''').fetchall())
