import sqlite3

conn = sqlite3.connect('./database.sqlite')

# conn.execute('CREATE TABLE todo (id INTEGER PRIMARY KEY AUTOINCREMENT, description TEXT NOT NULL, completed BOOLEAN DEFAULT false)')
conn.execute('INSERT INTO todo (description) VALUES ("test")')

conn.commit()

conn.close()