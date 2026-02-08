import sqlite3
from contextlib import closing

DB_PATH = "english_app.db"

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    with closing(get_conn()) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                email TEXT
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                module TEXT,
                score REAL,
                details TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        conn.commit()

def add_user(username, password, email):
    with closing(get_conn()) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                  (username, password, email))
        conn.commit()

def get_user(username):
    with closing(get_conn()) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        return c.fetchone()

def save_progress(user_id, module, score, details):
    with closing(get_conn()) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO progress (user_id, module, score, details) VALUES (?, ?, ?, ?)",
                  (user_id, module, score, details))
        conn.commit()

def get_progress(user_id):
    with closing(get_conn()) as conn:
        c = conn.cursor()
        c.execute("SELECT module, score, details, timestamp FROM progress WHERE user_id=?", (user_id,))
        return c.fetchall()
