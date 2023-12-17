import datetime

import psycopg
from flask_login import current_user
from werkzeug.security import generate_password_hash
from config import Config
from random import randint


class DBInterface():
    def getUserLogPassByID(self, user_id):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:
            cur = con.cursor()

            cur.execute('SELECT login, password FROM "user" WHERE id = %s',
                        [user_id])

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

            cur.execute('SELECT ID, login, password FROM "user" WHERE login = %s',
                        [login])

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
                print("Пользователь с такими данными уже зарегистрирован")
                return False

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

            print("Пользователь успешно зарегистрирован")
        return True

    def getCurrUserClient(self):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:
            cur = con.cursor()

            user_client = cur.execute('SELECT * FROM client WHERE user_id = %s',
                                      [current_user.id]).fetchone()
        if not user_client:
            return None
        return user_client

    def addClient(self, request):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:
            cur = con.cursor()

            res = self.getCurrUserClient()

            if res:
                print('Клиент уже существует')

            cur.execute('INSERT INTO client('
                        '"user_id",'
                        'phone_number,'
                        'full_name,'
                        'address,'
                        'birth_date) VALUES (%s, %s, %s, %s, %s)',
                        [
                            current_user.id,
                            request.form['phone_number'],
                            request.form['full_name'],
                            request.form['address'],
                            request.form['birth_date']
                        ]
                        )
            print('Клиент добавлен')

    def updateClient(self, request):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:
            cur = con.cursor()

            res = self.getCurrUserClient()

            if not res:
                print('Клиент не найден')
                return False

            cur.execute('UPDATE client SET'
                        ' phone_number = %s,'
                        ' full_name = %s,'
                        ' address = %s,'
                        ' birth_date = %s WHERE "user_id" = %s', [
                            request.form['phone_number'],
                            request.form['full_name'],
                            request.form['address'],
                            request.form['birth_date'],
                            current_user.id])

            print('Данные клиента обновлены')
            return True

    def getRoutes(self):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:

            cur = con.cursor()
            res = cur.execute('SELECT * FROM route').fetchall()

        if not res:
            print('Туры не найдены')
            return None
        return res

    def getCurrClientTrips(self):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:

            cur = con.cursor()

            client = self.getCurrUserClient()
            if not client:
                print('Клиент не найден')
                return None

            res = cur.execute('SELECT * FROM trip WHERE client_id = %s', [client[0]]).fetchall()

        if not res:
            print('Путевки не найдены')
            return None
        return res

    def getRouteByID(self, route_id):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:

            cur = con.cursor()

            res = cur.execute('SELECT * FROM route WHERE id = %s', [route_id]).fetchone()

        if not res:
            print('Маршрут с таким ID не найден')
            return None

        return res

    def getStationsByRouteID(self, route_id):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:

            cur = con.cursor()

            res = cur.execute('SELECT * FROM station INNER JOIN city ON station.city_id = city.id WHERE route_id = %s',
                              [route_id]).fetchall()

        if not res:
            print('Станции с таким route_id не найдены')
            return None

        return res

    def getHotelsByCity(self, city_id):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:

            cur = con.cursor()

            res = cur.execute('SELECT name FROM hotel WHERE city_id = %s',
                              [city_id]).fetchall()

        if not res:
            print('Отели в данном городе не найдены')
            return None

        return res

    def getСurrClientContracts(self):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:
            cur = con.cursor()

            client = self.getCurrUserClient()
            if not client:
                print('Клиент не найден')
                return None

            res = cur.execute('SELECT * FROM contract WHERE client_id = %s',
                              [client[1]]).fetchall()

        if not res:
            print('Договоры клиента не найдены')
            return None
        return res

    def addClientContract(self, request):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:
            cur = con.cursor()

            client = self.getCurrUserClient()
            curr_date = datetime.date.today()
            contract_number = randint(10000, 90000)

            if not client:
                print('Клиент не найден')
                return False

            cur.execute('INSERT INTO contract('
                        'client_id,'
                        'contract_number,'
                        'date_of_conclusion,'
                        'payment_method) VALUES (%s, %s, %s, %s)',
                        [
                            client[0],
                            contract_number,
                            curr_date,
                            request.form['payment_method'],
                        ]
                        )
            print('Контракт добавлен')

            return True

    def getContractByID(self, contract_id):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:
            cur = con.cursor()

            res = cur.execute('SELECT * FROM contract WHERE id = %s',
                              [contract_id]).fetchone()

        if not res:
            print('Контракт с таким id не найден')
            return None

        return res