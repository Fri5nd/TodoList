from flask import session
import sqlite3

if 'username' in session:
    username = session['username']
    conn = sqlite3.connect('users.sqlite')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()

conn = sqlite3.connect('./' + user + '.sqlite')

# conn.execute('CREATE TABLE todo (id INTEGER PRIMARY KEY AUTOINCREMENT, description TEXT NOT NULL, completed BOOLEAN DEFAULT false)')
conn.execute('INSERT INTO todo (description) VALUES ("test")')

conn.commit()

conn.close()
