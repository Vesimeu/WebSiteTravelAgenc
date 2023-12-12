from app import app, db
import psycopg
from flask import render_template, url_for, request, flash, redirect
from flask_login import current_user, login_user
from forms import RegistrationForm, LoginForm
from user import User
from werkzeug.security import check_password_hash


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        res = db.getUserByLogin(request.form['username'])

        if res is None or not check_password_hash(res[2], request.form['password']):
            flash('Неудачная попытка входа', 'error')
            return redirect(url_for('login'))

        ID, login, password = res
        user = User(ID, login, password)
        login_user(user, remember=login_form.remember_me.data)
        flash(f'Вы успешно авторизованы, {current_user.login}', 'success')
        return redirect(url_for('index'))

    return render_template('login.html', title='Авторизация', form=login_form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    reg_form = RegistrationForm()

    if reg_form.validate_on_submit():
        # enter user info to DB
            db.addUser(request)

            flash('Вы успешно зарегистрированы', 'success')
            return redirect(url_for('login'))
    return render_template('registration.html', title='Регистрация', form=reg_form)


@app.route('/testdb')
def test_connection():
    try:
        con = psycopg.connect(host=app.config['DB_SERVER'],
                              user=app.config['DB_USER'],
                              password=app.config['DB_PASSWORD'],
                              dbname=app.config['DB_NAME'])
    except Exception as e:
        message = f"Connection error: {e}"
        return message

    cur = con.cursor()
    cur.execute("SELECT * FROM HOTEL")
    message = cur.fetchall()

    return message


@app.route('/hotels')
def show_clients():
    with psycopg.connect(host=app.config['DB_SERVER'],
                         user=app.config['DB_USER'],
                         password=app.config['DB_PASSWORD'],
                         dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        hotel_names = cur.execute(f'SELECT name FROM hotel').fetchall()

    return render_template('hotels.html', title="Отели", hotel_names=hotel_names)
