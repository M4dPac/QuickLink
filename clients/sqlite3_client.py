import re
import sqlite3

from config import HOST
from generate import generate_random_string


class DatabaseManager:
    def __init__(self,
                 db_url: str = '../database.db',
                 creating: bool = False) -> None:
        '''
        Инициализация класса
        :param db_url: Адрес БД
        :param creating: Отвечает за создание таблицы
        '''
        self.db_url = db_url
        self.creating = creating

    def __len__(self):
        command = ''' SELECT COUNT(*) FROM links; '''
        self.execute_command(command)
        length = self.cursor.fetchone()
        return length[0] if length else 0

    def __enter__(self) -> 'DatabaseManager':
        self.conn = sqlite3.connect(self.db_url)
        self.cursor = self.conn.cursor()
        if self.creating:
            self.create_table()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.conn.commit()
        self.conn.close()

    def execute_command(self, command: str, params: tuple = ()) -> None:
        """Выполняет команду с параметрами"""
        if self.conn is None:
            raise ConnectionError('Database is not connected')
        self.cursor.execute(command, params)
        self.conn.commit()

    def create_table(self):
        command = '''
                CREATE TABLE IF NOT EXISTS links (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    short_url TEXT NOT NULL UNIQUE,
                    long_url TEXT NOT NULL
                    );
                    '''
        self.execute_command(command)

    def get_and_add_short_url(self, long_url: str) -> str:
        short_url = self._generate_short_url()
        command = f'''
        INSERT INTO links (short_url, long_url) VALUES (?, ?);
         '''
        self.execute_command(command, (short_url, long_url))
        return short_url

    def get_short_url(self, long_url: str) -> str:
        command = f'''
        SELECT short_url FROM links WHERE long_url = ?
        '''
        self.execute_command(command, (long_url,))
        answer = self.cursor.fetchone()
        if answer:
            return answer[0]

    def get_long_url(self, short_url: str) -> str:
        command = f'''
        SELECT long_url FROM links WHERE short_url = ?
        '''
        self.execute_command(command, (short_url,))
        answer = self.cursor.fetchone()
        if answer:
            return answer[0]

    def delete_url(self, url: str) -> None:
        command = f'''
        DELETE FROM links WHERE shorturl = ?;
        '''
        self.execute_command(command, (url,))

    def drop_table(self):
        commands = [
            "DELETE FROM links;",
            "DELETE FROM SQLITE_SEQUENCE WHERE name='links';",
        ]
        for command in commands:
            self.execute_command(command)

    def delete_table(self):
        command = ''' DROP TABLE links; '''
        self.execute_command(command)

    def _generate_short_url(self) -> str:
        while True:
            short_url = generate_random_string()
            if not self._is_in_db(short_url):
                return short_url

    def _is_in_db(self, short_url: str) -> bool:
        command = f'''
        SELECT short_url FROM links WHERE short_url = ?;
        '''
        self.execute_command(command, (short_url,))
        return bool(self.cursor.fetchone())


if __name__ == "__main__":
    with DatabaseManager('../test_database.db', creating=True) as client:
        short_url = client.get_and_add_short_url('google.com/')
        print(client.get_short_url('google.com/'))
        print(client.get_long_url(short_url))
        client.execute_command("SELECT * FROM links")
        print(client.cursor.fetchone())
        client.drop_table()
