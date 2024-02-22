from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

conn = sqlite3.connect('users.sqlite', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)''')
conn.commit()
conn.close()

def users():
    if 'username' in session:
        username = session['username']
        conn = sqlite3.connect('users.sqlite')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        conn.close()
        return user


def get_next_id():
    with sqlite3.connect('./database.sqlite') as con:
        cur = con.cursor()
        cur.execute("SELECT MAX(id) FROM todo")
        max_id = cur.fetchone()[0]
        return max_id + 1 if max_id is not None else 1

@app.route("/", methods=["POST", "GET"])
def home():
    user = users()
    if request.method == 'POST':
        try:
            desc = request.form['desc']
            task_id = get_next_id()

            with sqlite3.connect('./database.sqlite') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO todo (id, description) VALUES (?, ?)", (task_id, desc))
                con.commit()
        except Exception as e:
            print(e)
            con.rollback()
        finally:
            con.close()
            return redirect(url_for('home'))

    con = sqlite3.connect("database.sqlite")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM todo")

    rows = cur.fetchall()
    con.close()
    return render_template('index.html', rows=rows, user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    user = users()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.sqlite')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = c.fetchone()

        if user and check_password_hash(user[2], password):
            session['username'] = username
            flash('You have been successfully logged in.', 'success')
            conn.close()
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'error')
            conn.close()
            return redirect(url_for('login'))

    return render_template('login.html', user=user)



@app.route("/register", methods=['GET', 'POST'])
def register():
    user = users()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.sqlite')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        existing_user = c.fetchone()

        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
            conn.close()
            return redirect(url_for('register'))
        else:
            hashed_password = generate_password_hash(password)
            c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
            conn.close()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html', user=user)



@app.route("/toggle_completed/<int:task_id>", methods=["POST"])
def toggle_completed(task_id):
    with sqlite3.connect('./database.sqlite') as con:
        cur = con.cursor()
        cur.execute("UPDATE todo SET completed = NOT completed WHERE id = ?", (task_id,))
        con.commit()
    return redirect(url_for('home'))

@app.route("/remove_task/<int:task_id>", methods=["POST"])
def remove_task(task_id):
    with sqlite3.connect('./database.sqlite') as con:
        cur = con.cursor()
        cur.execute("DELETE FROM todo WHERE id = ?", (task_id,))
        con.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
