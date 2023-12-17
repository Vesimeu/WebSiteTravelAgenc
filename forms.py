from flask_wtf import FlaskForm
from wtforms import (BooleanField, StringField, DateField, IntegerField, PasswordField, SelectField, validators,
                     FormField, FieldList)


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', [validators.Length(min=4, max=25), validators.InputRequired()])
    email = StringField('E-mail', [validators.Length(min=6, max=100), validators.Email(), validators.InputRequired()])

    password = PasswordField('Пароль', [
        validators.InputRequired(),
        validators.Length(min=6, max=100),
        validators.EqualTo('confirm', message='Пароли должны совпадать')
    ])

    confirm = PasswordField('Повторите пароль')
    region_code = IntegerField('Код региона', [validators.InputRequired()])
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


class HotelsEntryForm(FlaskForm):
    hotels = SelectField('Отель', coerce=str)


class HotelsForm(FlaskForm):
    hotelsList = FieldList(FormField(HotelsEntryForm))
