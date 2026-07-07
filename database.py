import sqlite3
from pathlib import Path

Path("data").mkdir(exist_ok=True)

DB_PATH = "data/athena.db"


def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        datum TEXT,
        kilometer REAL,
        dauer REAL,
        pace TEXT,
        puls INTEGER,
        hoehenmeter INTEGER,
        kalorien INTEGER,
        notiz TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_run(datum, kilometer, dauer, pace, puls, hoehenmeter, kalorien, notiz):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO runs
    (datum, kilometer, dauer, pace, puls, hoehenmeter, kalorien, notiz)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datum,
        kilometer,
        dauer,
        pace,
        puls,
        hoehenmeter,
        kalorien,
        notiz
    ))

    conn.commit()
    conn.close()


def get_all_runs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT datum, kilometer, dauer, pace, puls, hoehenmeter, kalorien, notiz
    FROM runs
    ORDER BY id DESC
    """)

    runs = cursor.fetchall()
    conn.close()

    return runs


def get_last_three_runs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT datum, kilometer, dauer, pace, puls, hoehenmeter, kalorien, notiz
    FROM runs
    ORDER BY id DESC
    LIMIT 3
    """)

    runs = cursor.fetchall()
    conn.close()

    return runs