import re
import sqlite3

from config import HOST, DB_URL, TABLE_NAME
from generate import generate_random_string


class DatabaseManager:
    def __init__(self,
                 db_url: str = DB_URL,
                 *,
                 table_name: str = TABLE_NAME,
                 creating: bool = False) -> None:
        '''
        Class initialization
        :param db_url: The address of the database.
        :param table_name: The name of the table.
        :param creating: Responsible for creating the table.
        '''
        self.db_url = db_url
        self.table_name = table_name
        self.creating = creating

    def __len__(self):
        command = f''' SELECT COUNT(*) FROM {self.table_name}; '''
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
        if exc_type is not None:
            print(f"An error occurred: {exc_val}")
        self.conn.commit()
        self.conn.close()

    def execute_command(self, command: str, params: tuple = ()) -> None:
        """Executes a command with parameters"""
        if self.conn is None:
            raise ConnectionError('Database is not connected')
        try:
            self.cursor.execute(command, params)
            self.conn.commit()
        except sqlite3.Error:
            raise sqlite3.Error(f"An error occurred while executing the command: \n{command = }\n{params = }")

    def create_table(self):
        command = f'''
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    short_url TEXT NOT NULL UNIQUE,
                    long_url TEXT NOT NULL
                    );
                    '''
        self.execute_command(command)

    def get_and_add_short_url(self, long_url: str) -> str:
        short_url = self._generate_short_url()
        command = f'''
        INSERT INTO {self.table_name} (short_url, long_url) VALUES (?, ?);
         '''
        self.execute_command(command, (short_url, long_url))
        return short_url

    def get_short_url(self, long_url: str) -> str:
        command = f'''
        SELECT short_url FROM {self.table_name} WHERE long_url = ?
        '''
        self.execute_command(command, (long_url,))
        answer = self.cursor.fetchone()
        if answer:
            return answer[0]

    def get_long_url(self, short_url: str) -> str:
        command = f'''
        SELECT long_url FROM {self.table_name} WHERE short_url = ?
        '''
        self.execute_command(command, (short_url,))
        answer = self.cursor.fetchone()
        if answer:
            return answer[0]

    def delete_url(self, url: str) -> None:
        command = f'''
        DELETE FROM {self.table_name} WHERE shorturl = ?;
        '''
        self.execute_command(command, (url,))

    def drop_table(self):
        commands = [
            f"DELETE FROM {self.table_name};",
            f"DELETE FROM SQLITE_SEQUENCE WHERE name='{self.table_name}';",
        ]
        for command in commands:
            self.execute_command(command)

    def delete_table(self):
        command = f''' DROP TABLE {self.table_name}; '''
        self.execute_command(command)

    def _generate_short_url(self) -> str:
        while True:
            short_url = generate_random_string()
            if not self.is_url_in_db(short_url):
                return short_url

    def is_url_in_db(self, short_url: str) -> bool:
        command = f'''
        SELECT short_url FROM {self.table_name} WHERE short_url = ?;
        '''
        self.execute_command(command, (short_url,))
        return bool(self.cursor.fetchone())


if __name__ == "__main__":
    with DatabaseManager('../test_database.db', creating=True) as client:
        short_url = client.get_and_add_short_url('google.com/')
        print(client.get_short_url('google.com/'))
        print(client.get_long_url(short_url))
        client.execute_command(f"SELECT * FROM {TABLE_NAME}")
        print(client.cursor.fetchone())
        client.drop_table()
