import sqlite3


class DatabaseManager:
    def __init__(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_url TEXT NOT NULL,
            long_url TEXT NOT NULL
            )
            ''')
