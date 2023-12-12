import psycopg
from flask_login import current_user
from werkzeug.security import generate_password_hash
from config import Config


class DBInterface():
    def getUserLogPassByID(self, user_id):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:
            cur = con.cursor()

            cur.execute('SELECT login, password FROM "user" WHERE ID = %s', [user_id])

            result = cur.fetchone()

            if not result:
                print('Пользователь не найден')
                return None
            return result

    def getUserByLogin(self, login):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:
            cur = con.cursor()

            cur.execute('SELECT ID, login, password FROM "user" WHERE login = %s', [login])

            result = cur.fetchone()

            if not result:
                print('Пользователь не найден')
                return None
            return result

    def addUser(self, request):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:
            cur = con.cursor()

            res = cur.execute('SELECT * FROM "user" WHERE login = %s or email = %s',
                              [request.form['username'], request.form['email']]).fetchone()

            if res:
                message = "Пользователь с такими данными уже зарегистрирован"
                return message

            password_hash = generate_password_hash(request.form['password'])

            cur.execute(
                'INSERT INTO "user"('
                'login,'
                'email,'
                'password,'
                'region_code,'
                'want_spam) VALUES (%s, %s, %s, %s, %s)',
                [
                    request.form['username'],
                    request.form['email'],
                    password_hash, request.form['region_code'],
                    request.form['want_spam']
                ]
            )

            con.commit()

            message = "Пользователь успешно зарегистрирован"
        return message

    def getUserClient(self):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:
            cur = con.cursor()

            user_client = cur.execute('SELECT * FROM client WHERE user_id = %s', [current_user.id]).fetchall()

        return user_client

    def addClient(self, request):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:
            cur = con.cursor()

            user = self.getUserByLogin(current_user.login)

            cur.execute('INSERT INTO client('
                        '"user_id",'
                        'phone_number,'
                        'full_name,'
                        'address,'
                        'birth_date) VALUES (%s, %s, %s, %s, %s)',
                        [
                            user[0],
                            request.form['phone_number'],
                            request.form['full_name'],
                            request.form['address'],
                            request.form['birth_date']
                        ]
                        )
