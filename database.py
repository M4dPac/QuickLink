import re
import sqlite3

from config import HOST
from generate import generate_random_string


class DatabaseManager:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_url TEXT NOT NULL,
            long_url TEXT NOT NULL
            )
            ''')

    def add_short_url(self, long_url: str) -> str:
        short_url = self.__generate_short_url()
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
        answer = self.cursor.fetchone()
        if answer:
            return answer[0]

    def get_long_url(self, short_url: str) -> str:
        self.cursor.execute(f'''
        SELECT long_url FROM links WHERE short_url = '{short_url}'
        ''')
        answer = self.cursor.fetchone()
        if answer:
            return answer[0]

    def delete_url(self, url: str) -> None:
        if self.__is_host_url(url):
            self.cursor.execute(f'''
            DELETE FROM links WHERE shorturl = '{url}'
            ''')
        else:
            self.cursor.execute(f'''
            DELETE FROM links WHERE longurl = '{url}'
            ''')

    def __generate_short_url(self) -> str:
        while True:
            short_url = generate_random_string()
            if not self.__is_in_db(short_url):
                return short_url

    def __is_in_db(self, short_url: str) -> bool:
        self.cursor.execute(f'''
        SELECT short_url FROM links WHERE short_url = '{short_url}'
        ''')
        return bool(self.cursor.fetchone())

    def drop_table(self):
        self.cursor.execute(''' DROP TABLE IF EXISTS links ''')

    @staticmethod
    def __is_host_url(url: str) -> bool:
        return bool(re.match(rf"https*://{HOST}/", url))


if __name__ == "__main__":
    pass
