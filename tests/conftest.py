import pytest
import sqlite3

TEST_DB_URL = "../test_database.db"


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

    create_user_table_query = '''
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_url TEXT NOT NULL UNIQUE,
            long_url TEXT NOT NULL
            );
            '''

    drop_user_table_query = """
        DROP TABLE links;
    """

    db_connection.execute(create_user_table_query)
    db_connection.commit()
    yield
    db_connection.execute(drop_user_table_query)
    db_connection.commit()
