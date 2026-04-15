import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "..", "database", "college_system.db")


def authenticate(username, password):

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT role FROM users
        WHERE username=? AND password=?
    """, (username, password))

    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]
    else:
        return None