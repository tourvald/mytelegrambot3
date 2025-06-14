# storage/db.py

import sqlite3
from contextlib import closing
from datetime import datetime
import os

# Путь к базе данных
DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')


def initialize_database():
    # Инициализация базы данных и создание таблиц
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            # Удаление существующих таблиц, если они есть
            # conn.execute('DROP TABLE IF EXISTS queries')
            # conn.execute('DROP TABLE IF EXISTS prices')

            # Создание таблицы запросов
            conn.execute('''
                CREATE TABLE IF NOT EXISTS queries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    search_request TEXT NOT NULL,
                    url TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL
                )
            ''')

            # Создание таблицы цен с нужной структурой
            conn.execute('''
                CREATE TABLE IF NOT EXISTS prices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query_id INTEGER NOT NULL,
                    date TIMESTAMP NOT NULL,
                    price INTEGER NOT NULL,
                    FOREIGN KEY(query_id) REFERENCES queries(id)
                )
            ''')


def get_query_by_request_and_url(search_request, url):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM queries
            WHERE search_request = ? AND url = ?
        ''', (search_request, url))
        return cursor.fetchone()


def insert_query(search_request, url):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO queries (search_request, url, created_at)
            VALUES (?, ?, ?)
        ''', (search_request, url, datetime.now()))
        conn.commit()
        return cursor.lastrowid


def insert_price(query_id, price):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO prices (query_id, date, price)
            VALUES (?, ?, ?)
        ''', (query_id, datetime.now(), price))
        conn.commit()


def handle_query_and_price(search_request, url, avg_price):
    existing_query = get_query_by_request_and_url(search_request, url)
    if existing_query:
        query_id = existing_query[0]  # Используем ID существующего запроса
        insert_price(query_id, avg_price)
    else:
        query_id = insert_query(search_request, url)  # Создаем новый запрос
        insert_price(query_id, avg_price)


def get_last_10_prices_with_queries():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT prices.id, prices.date, prices.price, queries.search_request, queries.url
            FROM prices
            JOIN queries ON prices.query_id = queries.id
            ORDER BY prices.date DESC
            LIMIT 10
        ''')
        rows = cursor.fetchall()

        # Форматируем вывод
        for row in rows:
            print(f"Price ID: {row[0]}, Date: {row[1]}, Price: {row[2]}, "
                  f"Search Request: {row[3]}, URL: {row[4]}")

if __name__ == "__main__":
    get_last_10_prices_with_queries()