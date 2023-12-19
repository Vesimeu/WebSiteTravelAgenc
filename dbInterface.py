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

            cur.execute('SELECT login, password, role FROM "user" WHERE id = %s',
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

            cur.execute('SELECT ID, login, password, role FROM "user" WHERE login = %s',
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
                'role,'
                'is_banned) VALUES (%s, %s, %s, 2, False)',
                [
                    request.form['username'],
                    request.form['email'],
                    password_hash
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

            try:
                user_client = cur.execute('SELECT * FROM client WHERE user_id = %s',
                                          [current_user.id]).fetchone()
            except:
                print("Пользователь не найден")
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

    def getStationByID(self, station_id):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:
            cur = con.cursor()

            res = cur.execute('SELECT * FROM station INNER JOIN city ON station.city_id = city.id'
                              ' WHERE station.id = %s',
                              [station_id]).fetchone()

        if not res:
            print('Станции с таким id не найдены')
            return None

        return res

    def getHotelsByCity(self, city_id):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:
            cur = con.cursor()

            res = cur.execute('SELECT id, name FROM hotel WHERE city_id = %s',
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

    def getСurrClientContractsIDNumber(self):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:
            cur = con.cursor()

            client = self.getCurrUserClient()
            if not client:
                print('Клиент не найден')
                return None

            res = cur.execute('SELECT id, contract_number FROM contract WHERE client_id = %s',
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

    def getContractTrips(self, contract_id):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:
            cur = con.cursor()

            res = cur.execute('SELECT * FROM trip INNER JOIN route ON trip.group_id = route.id WHERE contract_id = %s',
                              [contract_id]).fetchall()

        if not res:
            print('Путевки с таким contract_id не найдены')
            return None

        return res

    def addClientTrip(self, request, route_id):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:
            cur = con.cursor()

            trip_number = randint(10000, 90000)
            route = self.getRouteByID(route_id)
            client = self.getCurrUserClient()
            tourist_group = self.getTouristGroupByRouteID(route_id)

            cur.execute('INSERT INTO trip('
                        'trip_number,'
                        'price,'
                        'group_id,'
                        'client_id,'
                        'contract_id) VALUES (%s, %s, %s, %s, %s)',
                        [
                            trip_number,
                            route[2],
                            tourist_group[0][0],
                            client[0],
                            request.form['choose_contract'],
                        ]
                        )
            print('Контракт добавлен')

            return True

    def getTouristGroupByRouteID(self, route_id):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:
            cur = con.cursor()

            res = cur.execute('SELECT * FROM tourist_group WHERE route_id = %s',
                              [route_id]).fetchall()

        if not res:
            print('Группы с таким route_id не найдены')
            return None
        return res

    def getExcursionsIDNameByCityID(self, city_id):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:
            cur = con.cursor()

            res = cur.execute('SELECT id, name FROM excursion WHERE city_id = %s',
                              [city_id]).fetchall()

        if not res:
            print('Экскурсии с таким city_id не найдены')
            return None
        return res

    def getClientTripsByRouteID(self, route_id):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:
            cur = con.cursor()

            res = cur.execute('SELECT trip.id, trip_number'
                              ' FROM trip INNER JOIN route ON trip.group_id = route.id WHERE route.id = %s',
                              [route_id]).fetchall()

        if not res:
            print('Путевки с таким route_id не найдены')
            return None
        return res

    def addHotelInTrip(self, request):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:
            cur = con.cursor()

            if self.getHotelInTripByID(request.form['choose_trip'], request.form['choose_hotel']):
                print('Данная отель уже добавлен в путевку')
                return False

            cur.execute('INSERT INTO hotel_in_trip('
                        'trip_id,'
                        'hotel_id) VALUES (%s, %s)',
                        [
                            request.form['choose_trip'],
                            request.form['choose_hotel']
                        ]
                        )
            print('Отель добавлен в путевку')

            return True

    def addExcursionInTrip(self, request):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:
            cur = con.cursor()

            if self.getExcursionInTripByID(request.form['choose_excursion'], request.form['choose_trip']):
                print('Данная экскурсия уже добавлена в путевку')
                return False

            cur.execute('INSERT INTO excursion_in_trip('
                        'trip_id,'
                        'excursion_id) VALUES (%s, %s)',
                        [
                            request.form['choose_trip'],
                            request.form['choose_excursion']
                        ]
                        )
            print('Экскурсия добавлена в путевку')

            return True

    def getExcursionInTripByID(self, excursion_id, trip_id):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:
            cur = con.cursor()

            res = cur.execute('SELECT * FROM excursion_in_trip'
                              ' WHERE excursion_id = %s AND trip_id = %s',
                              [excursion_id, trip_id]).fetchone()

        if not res:
            print('Экскурсии с таким id не найдены')
            return None
        return res

    def getHotelInTripByID(self, trip_id, hotel_id):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:
            cur = con.cursor()

            res = cur.execute('SELECT * FROM hotel_in_trip'
                              ' WHERE trip_id = %s AND hotel_id = %s',
                              [trip_id, hotel_id]).fetchone()

        if not res:
            print('Отели с таким id не найдены')
            return None
        return res

    def getExcursionInTripWithJoinsByID(self, trip_id):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:
            cur = con.cursor()

            res = cur.execute('SELECT * FROM excursion_in_trip '
                              'INNER JOIN excursion ON excursion_in_trip.excursion_id = excursion.id'
                              ' INNER JOIN city ON excursion.city_id = city.id'
                              ' WHERE trip_id = %s',
                              [trip_id]).fetchall()

        if not res:
            print('Отели с таким id не найдены')
            return None
        return res

    def getHotelInTripWithJoinsByID(self, trip_id):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:
            cur = con.cursor()

            res = cur.execute('SELECT * FROM hotel_in_trip '
                              'INNER JOIN hotel ON hotel_in_trip.hotel_id = hotel.id'
                              ' INNER JOIN city ON hotel.city_id = city.id'
                              '  WHERE trip_id = %s',
                              [trip_id]).fetchall()

        if not res:
            print('Отели с таким id не найдены')
            return None
        return res

    def getTripByID(self, trip_id):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:
            cur = con.cursor()

            res = cur.execute('SELECT * FROM trip WHERE id = %s',
                              [trip_id]).fetchone()

        if not res:
            print('Отели с таким id не найдены')
            return None
        return res

    def deleteTripByID(self, trip_id):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:
            cur = con.cursor()

            try:
                cur.execute('DELETE FROM excursion_in_trip WHERE trip_id = %s',
                              [trip_id])
                print('Экскурсии в путевке удалены')
            except:
                print('Экскурсии в путевке не найдены')

            try:
                cur.execute('DELETE FROM hotel_in_trip WHERE trip_id = %s', [trip_id])
                print('Отели в путевке удалены')
            except:
                print('Отели в путевке не найдены')

            try:
                cur.execute('DELETE FROM trip WHERE id = %s', [trip_id])
                print('Путевка удалена')
            except:
                print('Ошибка удаления путевки')