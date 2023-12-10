from app import app
import psycopg
from flask import render_template
from flask import request
from forms import RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    reg_form = RegistrationForm()

    if reg_form.validate_on_submit():
        # enter user info to DB
        with psycopg.connect(host=app.config['DB_SERVER'],
                             user=app.config['DB_USER'],
                             password=app.config['DB_PASSWORD'],
                             dbname=app.config['DB_NAME']) as con:
            cur = con.cursor()

            # data = cur.fetchall()

            ID = 1
            password_hash = generate_password_hash(request.form['password'])

            cur.execute(
                'INSERT INTO CLIENT('
                ' nick_name,'
                ' email,'
                ' hash_password,'
                ' region_code,'
                'want_spam,'
                'phone_number,'
                'full_name,'
                'address,'
                'date_of_birth) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                [request.form['username'], request.form['email'], password_hash, request.form['region_code'],
                 request.form['want_spam'], 0, '-', '-', request.form['birth_date']])

            con.commit()

        return 'Регистрация успешна'
    return render_template('registration.html', title='регистрация', form=reg_form)


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
