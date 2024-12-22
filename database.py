import sqlite3
import os
from parsing import parsing

DB_FILE = 'cars.db'


def create_database_and_table():
    if not os.path.exists(DB_FILE):
        print("Создание базы данных...")
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                years TEXT NOT NULL,
                body_color TEXT NOT NULL,
                int_color TEXT NOT NULL,
                body TEXT NOT NULL,
                engine TEXT NOT NULL,
                cnt_place TEXT NOT NULL,
                have TEXT NOT NULL,
                cost TEXT NOT NULL,
                image_url TEXT
            )
        """)

        conn.commit()
        cursor.close()
        conn.close()
        print("Таблица 'cars' успешно создана.")
    else:
        print("База данных 'cars.db' уже существует.")
    parsing()
