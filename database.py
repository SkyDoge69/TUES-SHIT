import sqlite3 as sqlite

DB_NAME = "example.db"

conn = sqlite.connect(DB_NAME)

conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS user
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        password TEXT NOT NULL,
        choice TEXT NOT NULL,
        rating DOUBLE,
        room_id TEXT NOT NULL
    )
''')
conn.commit()

conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS question
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        answer TEXT NOT NULL,
        user TEXT NOT NULL,
        FOREIGN KEY(user) REFERENCES user(name)
    )
''')
conn.commit()


class SQLite(object):

    def __enter__(self):
        self.conn = sqlite.connect(DB_NAME)
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()
