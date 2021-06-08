from flask import Flask, request, session,render_template,flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hexabyte'
app.permanent_session_lifetime = timedelta(hours=1)

def get_user_data(email):
    free = ''
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute(
        "SELECT user.id, user.name, user.lastname,login.email, login.password,roles.name , user.student, user.class, user.schoolname  FROM login INNER JOIN user ON login.email = user.email INNER JOIN roles on user.role_id = roles.id  INNER JOIN school ON user.student = school.role")
    users = cur.fetchall()
    con.close()
    for i in users:
        if email in i:
            free = i
    return free

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        curs = conn.cursor()
        curs.execute("SELECT * FROM login where email = (?)", [email])
        user = list(curs.fetchone())
        if email == user and check_password_hash(pss, password):
            session.permanent = True
            session['user'] = get_user_data(email)
            return render_template('index.html')

        else:
            flash('Email or password are wrong.')

    return render_template('login.html')