from flask import Flask, render_template, request, redirect, url_for, flash, session
import MySQLdb
import mysql.connector as db
import sqlalchemy
from flask_mysqldb import MySQL
from sqlalchemy import create_engine, false
from sqlalchemy.testing import db
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config["DEBUG"] = True


app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'super secret key'
conn = MySQLdb.connect(host="keepintouch24.mysql.pythonanywhere-services.com", user = "keepintouch24", passwd = "C0!!ege2014", db = "keepintouch24$napier_honours")
cursor = conn.cursor()

engine = sqlalchemy.create_engine('mysql+mysqlconnector://keepintouch24:C0!!ege2014@keepintouch24.mysql.pythonanywhere-services.com/keepintouch24$napier_honours')

@app.route('/login', methods=['GET', 'POST'])
def login_form(result=None):
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM users WHERE username = %s AND password = %s""", (username, password))
            info = cursor.fetchone()

            if info is not None:
                if info[1] == username and info[2] == password:
                    session['loginSuccess'] = True
                    session['username'] = username
                    session['info'] = info
                    session['result'] = result
                    return render_template('/recommendations.html', users=info, result=result)

        flash('Login unsuccessful. Please try again.')
    return render_template('/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == "POST":
        if "username" in request.form and "password" in request.form and "confirmPassword" \
                in request.form and "answer1" in request.form and "answer2" in request.form:
            username = request.form['username']
            password = request.form['password']

            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM users WHERE username = %s AND password = %s""", (username, password))
            info1 = cursor.fetchone()
            if info1 is not None:
                if info1['username'] == username:
                    flash('User already exist in database.')
                    return render_template('register.html')

            confirmpassword = request.form['confirmPassword']
            answer1 = request.form['answer1']
            answer2 = request.form['answer2']

            if password != confirmpassword:
                flash('Passwords do not matches. Please try again.')
                return render_template('register.html')
            else:
                cur = conn.cursor()
                cur.execute("INSERT INTO users(username,password, answer1, answer2)VALUES(%s, %s, %s, %s)",
                            (username, password, answer1, answer2))
                return render_template('login.html')

    return render_template('register.html')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/ketoScience.html')
def ketoScience():
    return render_template('ketoScience.html')


@app.route('/ketoPlan.html')
def ketoPlan():
    return render_template('ketoPlan.html')


@app.route('/recipes.html')
def recipes():
    return render_template('recipes.html')


@app.route('/books.html')
def books():
    return render_template('books.html')


@app.route('/login')
def login1():
    redirect(url_for('login'))
    session.pop('logged_in', True)


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/recommendations.html')
def recommendations():
    if session['loginSuccess']:
        username = session['username']
        info = session['info']
        result = session['result']
        return render_template('recommendations.html', users=info, result=result)
    else:
        return render_template('login.html')


@app.route('/recommendations', methods=['POST'])
def bmi(male=None, result=None, height=None, weight=None, age=None):
    if session['loginSuccess']:
        info = session['info']
        male = request.form['male']
        age = int(request.form['age'])
        height = int(request.form['height'])
        weight = int(request.form['weight'])

        if result is None:
            math = (weight / ((height / 100) * (height / 100)))
            if math < 18.5:
                result = 'You are underweight'
            elif math <= 24.9:
                result = 'You are healthy'
            elif math <= 29.9:
                result = 'You are over weight'
            elif math <= 34.9:
                result = 'You are severely over weight'
            elif math <= 39.9:
                result = 'You are obese'
            else:
                result = 'You are severely obese'
            flash(result)
            #print(math)
            #print(result)
            #info = session['info']
            session['result'] = result
            return render_template('recommendations.html', users=info, result=result, height=height,
                                   weight=weight, age=age, male=male)
        print(info)
        print(result)
        print(male)
        print(weight)
        print(height)
    return render_template('recommendations.html', users=info, result=result, height=height, weight=weight,
                           age=age, male=male)


@app.route('/logout')
def logout():
    session.clear()
    session['loginSuccess'] = False
    session.pop("username", None)
    return render_template('index.html')


if __name__ == '__main__':
    app.run()

