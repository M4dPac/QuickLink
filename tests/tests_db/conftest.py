import pytest
import sqlite3

from config import TEST_DB_URL, TABLE_NAME


@pytest.fixture(scope="session")
def db_connection():
    """Фикстура создаёт подключение к бд"""
    with sqlite3.connect(TEST_DB_URL) as connection:
        yield connection


@pytest.fixture(scope="session")
def db_cursor(db_connection):
    """Фикстура курсор для работы с бд"""
    cursor = db_connection.cursor()
    yield cursor


@pytest.fixture(scope="session", autouse=True)
def create_moderate_tables(db_connection):
    """Фикстура для создания и удаления таблицы"""

    create_user_table_query = f'''
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_url TEXT NOT NULL UNIQUE,
            long_url TEXT NOT NULL
            );
            '''

    drop_user_table_query = f"""
        DROP TABLE {TABLE_NAME};
    """

    db_connection.execute(create_user_table_query)
    db_connection.commit()
    yield
    db_connection.execute(drop_user_table_query)
    db_connection.commit()


@pytest.fixture(scope="function", autouse=True)
def clean_table(db_connection):
    """Фикстура для очистки бд"""
    commands = f"""
        DELETE FROM links;
        DELETE FROM SQLITE_SEQUENCE WHERE name='{TABLE_NAME}';
        """

    db_connection.executescript(commands)
    db_connection.commit()


@pytest.fixture(scope="session")
def create_test_url_in_database_function(db_connection):
    """Фикстура для создания функции для наполнения бд"""
    command = f"""
        INSERT INTO {TABLE_NAME} (short_url, long_url) VALUES (?, ?);
   """

    def create_url(short_url, long_url):
        """Функция для наполнения бд"""
        db_connection.execute(command, (short_url, long_url))
        db_connection.commit()

    return create_url


@pytest.fixture(scope="session")
def create_read_url_from_database_function(db_cursor):
    """Фикстура для создания функции для чтения из бд"""
    command = f"""
        SELECT * FROM {TABLE_NAME};
   """

    def read_url():
        """Функция для чтения из бд"""
        db_cursor.execute(command)
        return db_cursor.fetchall()

    return read_url
