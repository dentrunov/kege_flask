from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, HiddenField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import *


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField(
        'Подтверждение пароля', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Регистрация')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Пользователь с таким именем уже существует')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Такой адрес электронной почты уже существует')


class EditProfileForm(FlaskForm):
    groups_ = Groups.query.all()
    user_ = StringField('Имя', validators=[DataRequired()])
    role = SelectField('Выберите роль', choices=[(3, 'Ученик')])
    parent_email = StringField('Email родителя', validators=[DataRequired(), Email()])
    submit = SubmitField('Сохранить')


class EditAdminUserProfileForm(FlaskForm):
    groups_ = Groups.query.all()
    user_ = StringField('Имя', validators=[DataRequired()])
    role = SelectField('Выберите роль', choices=[(3, 'Ученик'), (4, 'Учитель'), (5, 'Родитель')])
    group = SelectField('Выберите группу', choices=[(group.group_id, group.gr_name) for group in groups_])
    submit = SubmitField('Сохранить')


class NewGroupForm(FlaskForm):
    gr_name = StringField('Название', validators=[DataRequired()])
    stud_year = SelectField('Выберите учебный год', choices=[(2022, '2022-2023'), (2023, '2023-2024')])
    submit = SubmitField('Сохранить')


class AnswerSimpleForm(FlaskForm):
    answerField = StringField('Ответ')
    answerNumber = HiddenField()
    submit = SubmitField('Сохранить')


class AnswerTwoForm(FlaskForm):
    answerField1 = StringField('Ответ')
    answerField2 = StringField('Ответ')
    answerNumber = HiddenField()
    submit = SubmitField('Сохранить')


class AnswerManyForm(FlaskForm):
    answerField1 = StringField('Ответ')
    answerField2 = StringField('Ответ')
    answerField3 = StringField('Ответ')
    answerField4 = StringField('Ответ')
    answerField5 = StringField('Ответ')
    answerField6 = StringField('Ответ')
    answerField7 = StringField('Ответ')
    answerField8 = StringField('Ответ')
    answerField9 = StringField('Ответ')
    answerField10 = StringField('Ответ')
    answerNumber = HiddenField()
    submit = SubmitField('Сохранить')


class AddNewTest(FlaskForm):
    pathField = StringField('Путь к папке теста')
    testnameField = StringField('Название теста')
    for i in range(1, 28):
        locals()['task_Field'+str(i)] = StringField('Задание ' + str(i))
    submit = SubmitField('Сохранить')


class AddVideoForm(FlaskForm):
    video_link = StringField('Ссылка на видео')
    video_name = StringField('Название видео')
    video_text = TextAreaField('Описание видео')
    submit = SubmitField('Сохранить')
