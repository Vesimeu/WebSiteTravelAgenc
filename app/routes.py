from app import app
import psycopg
from flask import render_template

@app.route('/index')
def index():
    return render_template('index.html')

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
