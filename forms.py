from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, DateField, IntegerField, PasswordField, validators


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', [validators.Length(min=4, max=25), validators.InputRequired()])
    email = StringField('E-mail', [validators.Length(min=6, max=100), validators.Email(), validators.InputRequired()])

    password = PasswordField('Пароль', [
        validators.InputRequired(),
        validators.Length(min=6, max=100),
        validators.EqualTo('confirm', message='Пароли должны совпадать')
    ])

    confirm = PasswordField('Повторите пароль')
    birth_date = DateField('Дата рождения', [validators.InputRequired()], '%Y-%m-%d')
    region_code = IntegerField('Код региона', [validators.InputRequired()])
    want_spam = BooleanField('Я согласен получать рекламную рассылку', [validators.InputRequired()])


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', [validators.Length(min=4, max=25), validators.InputRequired()])
    password = PasswordField('Пароль', [
        validators.InputRequired(),
        validators.Length(min=6, max=100),
    ])
