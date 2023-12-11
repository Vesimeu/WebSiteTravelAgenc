from app import app, login_manager, login_user, db
import psycopg
from flask import render_template, url_for
from flask import request, flash, redirect
from forms import RegistrationForm, LoginForm
from userLogin import UserLogin
from werkzeug.security import check_password_hash


@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    print(user_id)

    return UserLogin().fromDb(user_id, db)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user = db.getUserByLogin(request.form['username'])

        if user and check_password_hash(user[0][3], request.form['password']):
            userLogin = UserLogin().create(user)
            login_user(userLogin)

            flash('Вы успешно авторизованы', 'success')
            return redirect(url_for('index'))
        flash('Пароль/имя пользователя введены неверно', 'error')

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
