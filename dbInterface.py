import psycopg
from werkzeug.security import generate_password_hash
from config import Config


class DBInterface():
    def getUserInfo(self, user_id):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:
            cur = con.cursor()

            cur.execute('SELECT * FROM "user" WHERE ID = %s LIMIT 1', [user_id])

            result = cur.fetchall()

            if not result:
                print('Пользователь не найден')
                return False
            return result

    def getUserByLogin(self, login):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:
            cur = con.cursor()

            cur.execute('SELECT * FROM "user" WHERE login = %s LIMIT 1', [login])

            result = cur.fetchall()

            if not result:
                print('Пользователь не найден')
                return False
            return result

    def addUser(self, request):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:
            cur = con.cursor()

            password_hash = generate_password_hash(request.form['password'])

            cur.execute(
                'INSERT INTO "user"('
                'login,'
                'email,'
                'password,'
                'region_code,'
                'want_spam,'
                'date_of_birth) VALUES (%s, %s, %s, %s, %s, %s)',
                [request.form['username'], request.form['email'], password_hash, request.form['region_code'],
                 request.form['want_spam'], request.form['birth_date']])

            con.commit()
