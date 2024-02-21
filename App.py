from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route("/", methods = ["POST", "GET"])
def home():
    if request.method == 'POST':
        try:
            desc = request.form['desc']

            with sqlite3.connect('./database.sqlite') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO todo (description) VALUES (?)",(desc,))

                con.commit()
        except:
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
    return render_template('index.html', rows=rows)

@app.route("/login")
def login():
    return render_template('login.html')

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