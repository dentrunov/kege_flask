from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, HiddenField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import *

from string import ascii_letters, digits, punctuation

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=8)])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=6, max=12, message='Имя пользователя должно быть не менее %(min)d, и не более %(max)d символов')])
    user_ = StringField('Ваше имя (и фамилия)', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField(
        'Подтверждение пароля', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Регистрация')


    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Пользователь с таким именем уже существует')
        included_chars = ascii_letters + digits + punctuation
        for char in self.username.data:
            if not (char in included_chars):
                raise ValidationError(
                    f"Символ {char} нельзя использовать")

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Такой адрес электронной почты уже существует')


class forgerPwdForm(FlaskForm):
    text = StringField('Имя пользователя или почта', validators=[DataRequired()])
    submit = SubmitField('Отправить')


class newPassForm(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField(
        'Подтверждение пароля', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Сохранить')

class EditProfileForm(FlaskForm):
    groups_ = Groups.query.all()
    user_ = StringField('Имя', validators=[DataRequired()])
    role = SelectField('Выберите роль', choices=[(3, 'Ученик')])
    parent_email = StringField('Email родителя', validators=[Email()])
    submit = SubmitField('Сохранить')