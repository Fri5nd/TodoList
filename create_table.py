import sqlite3

conn = sqlite3.connect('./database.db')

conn.execute('CREATE TABLE todo (id INTEGER PRIMARY KEY AUTOINCREMENT, description TEXT NOT NULL, completed BOOLEAN NOT NULL DEFAULT false)')