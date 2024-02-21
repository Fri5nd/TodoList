from flask import Flask
from flask import render_template
from flask import request
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    con = sqlite3.connect("database.sqlite")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM todo")

    rows = cur.fetchall()
    con.close()
    return render_template('index.html', rows=rows)

@app.route("/addtask")
def addtask():
    return render_template('addtask.html')

@app.route("/addta", methods = ["POST", "GET"])
def addta():
    if request.method == 'POST':
        try:
            desc = request.form['desc']

            with sqlite3.connect('./database.sqlite') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO todo (description) VALUES (?)",(desc,))

                con.commit()
                msg = "Record successfully added to database"
        except:
            con.rollback()
            msg = "Error in the INSERT"

        finally:
            con.close()
            return render_template('result.html',msg=msg)

@app.route("/login")
def login():
    return render_template('login.html')


if __name__ == "__main__": 
    app.run(debug=True)