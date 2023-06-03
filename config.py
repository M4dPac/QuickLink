from dotenv import load_dotenv
import os

load_dotenv()

HOST = os.getenv("HOST")
TABLE_NAME = "links"
DB_URL = "../database.db"

# Данные для тестов
TEST_DB_URL = "../test_database.db"
