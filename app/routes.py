from app import app, db
from flask import render_template, url_for, request, flash, redirect
from flask_login import current_user, login_user, logout_user
from forms import (RegistrationForm, LoginForm, EditProfileForm, ContractForm, TripForm, HotelForm, ExcursionForm,
                   BanUserForm, UnbanUserForm, GroupForm, AddGropToTripFrom)
from user import User
from werkzeug.security import check_password_hash


@app.route('/')
def index():
    routes = db.getRoutes()

    return render_template('index.html', routes=routes, title='Доступные туры')


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user_result = db.getUserByLogin(request.form['username'])

        if user_result is None or not check_password_hash(user_result[2], request.form['password']):
            flash('Неверное имя пользователя или пароль', 'error')
            return redirect(url_for('login'))

        id, login, password, role, is_banned = user_result
        if user_result[4]:
            flash('Данный пользователь заблокирован администратором', 'error')
            return redirect(url_for('login'))

        user = User(id, login, password, role)
        login_user(user, remember=login_form.remember_me.data)
        flash(f'Вы успешно авторизованы, {current_user.login}', 'success')

        return redirect(url_for('profile'))
    return render_template('login.html', title='Авторизация', form=login_form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    reg_form = RegistrationForm()

    if reg_form.validate_on_submit():
        if not db.addUser(request):
            flash('Неудачная попытка регистрации !'
                  ' Пользователь с таким email/login уже зарегистрирован',
                  'danger')
            return redirect(url_for('register'))
        flash('Пользователь успешно зарегистрирован', 'success')
        return redirect(url_for('login'))
    return render_template('registration.html', title='Регистрация', form=reg_form)


@app.route('/profile')
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    user_client = db.getCurrUserClient()
    return render_template('profile.html', title='Мой профиль', user_client=user_client)


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    edit_profile_form = EditProfileForm()
    client = db.getCurrUserClient()

    if request.method == 'GET':
        if client:
            edit_profile_form.phone_number.data = client[2]
            edit_profile_form.full_name.data = client[3]
            edit_profile_form.address.data = client[4]
            edit_profile_form.birth_date.data = client[5]

    if edit_profile_form.validate_on_submit():
        if client:
            db.updateClient(request)
        else:
            db.addClient(request)

        flash('Информация успешно обновлена', 'success')
        return redirect(url_for('profile'))

    return render_template('edit_profile.html', title='Редактировать профиль', form=edit_profile_form)


@app.route('/contracts', methods=['GET', 'POST'])
def contracts():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    contract_form = ContractForm()
    res_contracts = db.getСurrClientContracts()

    if contract_form.validate_on_submit():
        if not db.addClientContract(request):
            flash('Для заключения контракта вам необходимо заполнить профиль', 'danger')
            return redirect(url_for('edit_profile'))
        return redirect(url_for('contracts'))

    return render_template('contracts.html',
                           title='Мои договоры', form=contract_form, contracts=res_contracts)


@app.route('/contract/<int:contract_id>')
def view_contract(contract_id):
    contract = db.getContractByID(contract_id)
    contract_trips = db.getContractTrips(contract_id)

    return render_template('trips.html', contract=contract, contract_trips=contract_trips)


@app.route('/contract/<int:contract_id>/delete_trip/<trip_id>', methods=['POST'])
def delete_trip(trip_id, contract_id):
    db.deleteTripByID(trip_id)
    return redirect(url_for('view_contract', contract_id=contract_id))


@app.route('/contract/<int:contract_id>/trip/<int:trip_id>')
def view_trip(contract_id, trip_id):
    excursions = db.getExcursionInTripWithJoinsByID(trip_id)
    hotels = db.getHotelInTripWithJoinsByID(trip_id)
    trip = db.getTripByID(trip_id)

    return render_template('trip.html', excursions=excursions, hotels=hotels, trip=trip)


@app.route('/route/<int:route_id>', methods=['GET', 'POST'])
def view_route(route_id):
    route = db.getRouteByID(route_id)
    stations = db.getStationsByRouteID(route_id)
    contracts_res = db.getСurrClientContractsIDNumber()

    if not contracts_res and current_user.is_authenticated:
        flash('Для бронирования путевки необходимо заключить договор', 'danger')
        return redirect(url_for('contracts'))

    trip_form = TripForm()
    trip_form.choose_contract.choices = contracts_res

    if trip_form.validate_on_submit():
        db.addClientTrip(request, route_id)
        flash('Путевка успешно забронирована', 'success')

    return render_template('route.html', titile='Просмотр тура',
                           route=route, stations=stations, form=trip_form)


@app.route('/route/<int:route_id>/station/<int:station_id>', methods=['GET', 'POST'])
def view_station(route_id, station_id):
    client = db.getCurrUserClient()
    if not client:
        flash('Для конфигурирования путевки необходимо заполнить профиль', 'danger')
        return redirect(url_for('profile'))

    trips = db.getClientTripsByRouteID(route_id)
    if not trips:
        flash('Для конфигурирования путевки ее необходимо забронировать', 'danger')
        return redirect(url_for('view_route', route_id=route_id))

    station = db.getStationByID(station_id)
    hotels = db.getHotelsByCity(station[4])
    excursions_id_name = db.getExcursionsIDNameByCityID(station[4])

    hotel_form = HotelForm()
    excursion_form = ExcursionForm()

    if trips:
        hotel_form.choose_trip.choices = trips
        excursion_form.choose_trip.choices = trips
    else:
        hotel_form.choose_trip.choices = [0, 'null']
        excursion_form.choose_trip.choices = [0, 'null']
    if hotels:
        hotel_form.choose_hotel.choices = hotels
    else:
        hotel_form.choose_hotel.choices = [0, 'null']
    if excursions_id_name:
        excursion_form.choose_excursion.choices = excursions_id_name
    else:
        excursion_form.choose_excursion.choices = [0, 'null']

    if hotel_form.validate_on_submit():
        if db.addHotelInTrip(request):
            flash('Отель успешно добавлен в путевку', 'success')
        else:
            flash('Данный отель уже есть путевке', 'danger')

    if excursion_form.validate_on_submit():
        if db.addExcursionInTrip(request):
            flash('Экскурсия добавлена в путевку', 'success')
        else:
            flash('Данная экскурсия уже есть путевке', 'danger')

    return render_template('station.html', station=station, hotels=hotels,
                           excursions=excursions_id_name, hotel_form=hotel_form, excursion_form=excursion_form)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if current_user.role != 1:
        flash('Вы не являетесь администратором', 'danger')
        return redirect(url_for('index'))

    users = db.getUsers()
    routes = db.getRoutesIDName()
    trips = db.getTrips()
    groups = db.getGroups()

    group_form = GroupForm()
    ban_form = BanUserForm()
    unban_form = UnbanUserForm()
    group_trip_form = AddGropToTripFrom()

    if users:
        ban_form.choose_user.choices = users
        unban_form.choose_login.choices = users
    else:
        ban_form.choose_user.choices = [0, 'null']
        unban_form.choose_login.choices = [0, 'null']

    if routes:
        group_form.choose_route.choices = routes
    else:
        group_form.choose_route.choices = [0, 'null']

    if trips:
        group_trip_form.choose_trip.choices = trips
    else:
        group_trip_form.choose_trip.choices = [0, 'null']

    if groups:
        group_trip_form.choose_group.choices = groups
    else:
        group_trip_form.choose_group.choices = [0, 'null']

    if group_form.validate_on_submit():
        db.addGroup(request)
        flash('Группа добавлена', 'success')

    if ban_form.validate_on_submit():
        db.banUser(request.form['choose_user'])
        flash('Пользователь забанен', 'success')

    if unban_form.validate_on_submit():
        db.unbanUser(request.form['choose_login'])
        flash('Пользователь разбанен', 'success')

    if group_trip_form.validate_on_submit():
        db.changeTripGroup(request)

    return render_template('admin.html', ban_form=ban_form, unban_form=unban_form,
                           group_form=group_form, group_trip_form=group_trip_form)
