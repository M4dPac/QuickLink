import pytest
import sqlite3

from clients.sqlite3_client import DatabaseManager

TEST_DB_URL = "../test_database.db"

# Запрос для создания таблицы
CREATE_USER_TABLE_QUERY = '''
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_url TEXT NOT NULL,
            long_url TEXT NOT NULL
            )
            '''

# Запрос для сброса таблицы
DROP_USER_TABLE_QUERY = '''
        DROP TABLE IF EXISTS links
            '''


def test_write_to_db_by_command():
    """
    Создаем независимое подключение к бд, выполняем команду для создания таблицы
    :return: None
    """
    with sqlite3.connect(TEST_DB_URL) as db_connection:
        db_connection.execute(DROP_USER_TABLE_QUERY)
        cursor = db_connection.cursor()
        db_connection.execute(CREATE_USER_TABLE_QUERY)
        db_connection.commit()

    command = f'''
    INSERT INTO links (short_url, long_url) VALUES (?, ?)
    '''
    short_url = 'CEBzLX'
    long_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'

    # Создаем клиент
    with DatabaseManager(TEST_DB_URL) as client:
        # Делаем запись в бд
        client.execute_command(command, (short_url, long_url))
        client.drop_table()


if __name__ == '__main__':
    pytest.main()
