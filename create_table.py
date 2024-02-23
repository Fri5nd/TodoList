from flask import session
import sqlite3

# if 'username' in session:
#     username = session['username']
#     conn = sqlite3.connect('users.sqlite')
#     c = conn.cursor()
#     c.execute('SELECT * FROM users WHERE username = ?', (username,))
#     user = c.fetchone()
#     conn.close()

conn = sqlite3.connect('./db/mydb.sqlite')

conn.execute(f'''CREATE TABLE IF NOT EXISTS todo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                userid INTEGER NOT NULL, 
                description TEXT NOT NULL, 
                completed BOOLEAN DEFAULT false
            )''')

conn.execute('''
CREATE TABLE IF NOT EXISTS users (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             username TEXT NOT NULL,
             password TEXT NOT NULL
)
''')
# conn.execute('INSERT INTO todo (description) VALUES ("test")')

conn.commit()

conn.close()
