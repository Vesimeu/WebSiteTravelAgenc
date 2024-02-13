from flask_wtf import FlaskForm
from wtforms import (BooleanField, StringField, DateField, IntegerField, PasswordField, SelectField, validators,
                     DecimalField)


# Форма регистрации
class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', [validators.Length(min=4, max=25), validators.InputRequired()])
    email = StringField('E-mail', [validators.Length(min=6, max=100), validators.Email(), validators.InputRequired()])

    password = PasswordField('Пароль', [
        validators.InputRequired(),
        validators.Length(min=6, max=100),
        validators.EqualTo('confirm', message='Пароли должны совпадать')
    ])

    confirm = PasswordField('Повторите пароль')


# Форма авторизации
class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', [validators.Length(min=4, max=25), validators.InputRequired()])
    password = PasswordField('Пароль', [
        validators.InputRequired(),
        validators.Length(min=6, max=100),
    ])
    remember_me = BooleanField('Запомнить меня')


# Форма редактирования профиля
class EditProfileForm(FlaskForm):
    full_name = StringField('ФИО клиента', [validators.InputRequired()])
    birth_date = DateField('Дата рождения', format='%Y-%m-%d', validators=[validators.InputRequired()])
    address = StringField('Адрес', [validators.InputRequired()])
    phone_number = StringField('Номер телефона', [validators.Length(min=6, max=12), validators.InputRequired()])


# Форма заключения контракта
class ContractForm(FlaskForm):
    payment_method = SelectField('Способ оплаты',
                                 choices=[('Банковская карта', 'Банковская карта'), ('Наличные', 'Наличные')],
                                 validate_choice=True)
    agreed_rules = BooleanField('Я ознакомлен с политикой компании', [validators.InputRequired()])


# Форма бронирования путевки
class TripForm(FlaskForm):
    choose_contract = SelectField('Выберите номер договора')


# Форма бронирования отеля
class HotelForm(FlaskForm):
    choose_trip = SelectField('Выберите номер путевки')
    choose_hotel = SelectField('Выберите отель')


# Форма выбора экскурсии
class ExcursionForm(FlaskForm):
    choose_trip = SelectField('Выберите номер путевки')
    choose_excursion = SelectField('Выберите экскурсию')


# Форма блокировки пользователя
class BanUserForm(FlaskForm):
    choose_user = SelectField('Выберите логин пользователя')


# Форма разблокировки пользователя
class UnbanUserForm(FlaskForm):
    choose_login = SelectField('Выберите логин пользователя')


# Форма  добавления группы
class GroupForm(FlaskForm):
    choose_route = SelectField('Выберите тур для группы')
    travel_date = DateField('Дата поездки', format='%Y-%m-%d', validators=[validators.InputRequired()])


# Форма добавления группы в путевку
class AddGropToTripFrom(FlaskForm):
    choose_trip = SelectField('Выберите путевку')
    choose_group = SelectField('Выберите группу')


# Форма добавления тура
class RouteForm(FlaskForm):
    name = StringField('Название тура', [validators.InputRequired()])
    price = DecimalField('Стоимость', [validators.InputRequired()])
    duration = IntegerField('Длительность', [validators.InputRequired()])
    start_date = DateField('Дата начала поездки', format='%Y-%m-%d', validators=[validators.InputRequired()])
    end_date = DateField('Дата окончания поездки', format='%Y-%m-%d', validators=[validators.InputRequired()])


# Форма добавления пункта назначения
class StationForm(FlaskForm):
    name = StringField('Название пункта назначения', [validators.InputRequired()])
    duration = IntegerField('Длительность', [validators.InputRequired()])
    country = SelectField('Выберите страну')
