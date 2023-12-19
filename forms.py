from flask_wtf import FlaskForm
from wtforms import (BooleanField, StringField, DateField, IntegerField, PasswordField, SelectField, validators)


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', [validators.Length(min=4, max=25), validators.InputRequired()])
    email = StringField('E-mail', [validators.Length(min=6, max=100), validators.Email(), validators.InputRequired()])

    password = PasswordField('Пароль', [
        validators.InputRequired(),
        validators.Length(min=6, max=100),
        validators.EqualTo('confirm', message='Пароли должны совпадать')
    ])

    confirm = PasswordField('Повторите пароль')
    want_spam = BooleanField('Я согласен получать рекламную рассылку', [validators.InputRequired()])


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', [validators.Length(min=4, max=25), validators.InputRequired()])
    password = PasswordField('Пароль', [
        validators.InputRequired(),
        validators.Length(min=6, max=100),
    ])
    remember_me = BooleanField('Запомнить меня')


class EditProfileForm(FlaskForm):
    full_name = StringField('ФИО клиента', [validators.InputRequired()])
    birth_date = DateField('Дата рождения', format='%Y-%m-%d', validators=[validators.InputRequired()])
    address = StringField('Адрес', [validators.InputRequired()])
    phone_number = StringField('Номер телефона', [validators.Length(min=6, max=12), validators.InputRequired()])


class ContractForm(FlaskForm):
    payment_method = SelectField('Способ оплаты', choices=[('Банковская карта', 'Банковская карта'), ('Наличные', 'Наличные')],
                                 validate_choice=True)
    agreed_rules = BooleanField('Я ознакомлен с политикой компании', [validators.InputRequired()])


class TripForm(FlaskForm):
    choose_contract = SelectField('Выберите номер договора')


class HotelForm(FlaskForm):
    choose_trip = SelectField('Выберите номер путевки')
    choose_hotel = SelectField('Выберите отель')


class ExcursionForm(FlaskForm):
    choose_trip = SelectField('Выберите номер путевки')
    choose_excursion = SelectField('Выберите экскурсию')


class BanUserForm(FlaskForm):
    choose_user = SelectField('Выберите логин пользователя')


class UnbanUserForm(FlaskForm):
    choose_login = SelectField('Выберите логин пользователя')
