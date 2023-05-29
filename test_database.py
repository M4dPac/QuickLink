import pytest

from database import DatabaseManager

long_link = "https://www.google.com"


@pytest.fixture
def db_manager():
    return DatabaseManager()


@pytest.fixture
def db(db_manager):
    db_manager.add_short_url(long_link)
    yield db

    db.cursor.close()
    db.conn.close()


@pytest.fixture
def short_link(db):
    pass


class TestDatabase:
    def test_get_short_url(self, db):
        current_link = db.get_short_url(long_link)
        assert current_link == self.short_link, \
            f"Wrong short link, curent link: {current_link}, expected link: {self.short_link}"

    def test_get_long_url(self, db):
        current_link = db.get_long_url(self.short_link)
        assert current_link == long_link, \
            f"Wrong long link, curent link: {current_link}, expected link: {long_link}"

    def test_delete_short_url(self, db):
        db.delete_short_url(self.short_link)
        current_link = db.get_long_url(self.short_link)
        assert current_link is None

    def test_get_wrong_url(self, db):
        assert db.get_short_url("https://www.mail.ru") is None


if __name__ == "__main__":
    pytest.main()
