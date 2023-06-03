import pytest

from clients.sqlite3_client import DatabaseManager
from tests.conftest import TEST_DB_URL


def test_write_to_db_by_command(create_read_url_from_database_function):
    """
    Создаем независимое подключение к бд, выполняем команду для создания таблицы.
    С помощью клиента делаем запись в бд и проверяем результат.
    """

    long_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
    # Создаем клиент
    with DatabaseManager(TEST_DB_URL) as client:
        # Генерируем короткую ссылку
        short_url = client.get_and_add_short_url(long_url)

    # Проверяем результат

    links = create_read_url_from_database_function()

    assert len(links) == 1
    assert links[0][1] == short_url
    assert links[0][2] == long_url


def test_read_from_db_client(create_test_url_in_database_function,
                             create_read_url_from_database_function):
    """
    Создаем независимое подключение к бд, выполняем команду для создания таблицы, записываем данные.
    С помощью клиента проверяем результат.
    """

    short_url = 'CEBzuX'
    long_url = 'https://www.youtube.com/watch?v=dQw4w9WgXtQ'

    create_test_url_in_database_function(short_url, long_url)

    # Создаем клиент
    with DatabaseManager(TEST_DB_URL) as client:
        # Считываем данные из бд
        current_short_link = client.get_short_url(long_url)
        current_long_link = client.get_long_url(short_url)
        curent_length = len(client)

    # Проверяем результат
    links = create_read_url_from_database_function()

    assert len(links) == curent_length
    assert current_short_link == short_url
    assert current_long_link == long_url


if __name__ == '__main__':
    pytest.main()
