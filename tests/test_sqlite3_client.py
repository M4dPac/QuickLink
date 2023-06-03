import pytest
import sqlite3

from clients.sqlite3_client import DatabaseManager

TEST_DB_URL = "../test_database.db"
DB_CONNECTION = sqlite3.connect(TEST_DB_URL)
DB_CURSOR = DB_CONNECTION.cursor()


def create_url(short_url: str, long_url: str):
    """ Функция для наполнения бд тестовыми данными"""
    command = f'''
            INSERT INTO links (short_url, long_url) VALUES (?, ?);
            '''
    DB_CURSOR.execute(command, (short_url, long_url))
    DB_CONNECTION.commit()


def read_table():
    """ Функция для чтения из бд"""
    command = f'''
            SELECT * FROM links;
            '''
    DB_CURSOR.execute(command)
    return DB_CURSOR.fetchall()


def create_table():
    """ Функция для создания таблицы"""
    command = f'''
            CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_url TEXT NOT NULL,
            long_url TEXT NOT NULL
            );
            '''
    DB_CURSOR.execute(command)
    DB_CONNECTION.commit()


def drop_table():
    """ Функция для удаления таблицы"""
    command = f'''
            DELETE FROM links;
            '''
    DB_CURSOR.execute(command)
    DB_CONNECTION.commit()


def test_write_to_db_by_command():
    """
    Создаем независимое подключение к бд, выполняем команду для создания таблицы.
    С помощью клиента делаем запись в бд и проверяем результат.
    :return: None
    """

    long_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
    # Создаем клиент
    with DatabaseManager(TEST_DB_URL) as client:
        # Генерируем короткую ссылку
        short_url = client.get_and_add_short_url(long_url)

    # Проверяем результат

    links = read_table()

    assert len(links) == 1
    assert links[0][1] == short_url
    assert links[0][2] == long_url



def test_read_from_db_client():
    """
    Создаем независимое подключение к бд, выполняем команду для создания таблицы, записываем данные.
    С помощью клиента проверяем результат.
    :return: None
    """

    short_url = 'CEBzuX'
    long_url = 'https://www.youtube.com/watch?v=dQw4w9WgXtQ'

    create_url(short_url, long_url)

    # Создаем клиент
    with DatabaseManager(TEST_DB_URL) as client:
        # Считываем данные из бд
        current_short_link = client.get_short_url(long_url)
        current_long_link = client.get_long_url(short_url)
        curent_length = len(client)

    # Проверяем результат
    links = read_table()

    assert len(links) == curent_length
    assert current_short_link == short_url
    assert current_long_link == long_url


if __name__ == '__main__':
    pytest.main()
