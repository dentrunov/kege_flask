from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import Users, Groups, Test_started, Tests


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
    role = SelectField('Выберите роль', choices=[(3, 'Ученик'), (4, 'Учитель'), (5, 'Родитель')])
    #group = SelectField('Выберите группу', choices=[(group.group_id, group.gr_name) for group in groups_])
    submit = SubmitField('Сохранить')


class NewGroupForm(FlaskForm):
    gr_name = StringField('Название', validators=[DataRequired()])
    stud_year = SelectField('Выберите учебный год', choices=[(2022, '2022-2023'), (2023, '2023-2024')])
    submit = SubmitField('Сохранить')


class AnswerSimpleForm(FlaskForm):
    answerField = StringField('Ответ')
    submit = SubmitField('Сохранить')

class AnswerTwoForm(FlaskForm):
    answerField1 = StringField('Ответ')
    answerField2 = StringField('Ответ')
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
    submit = SubmitField('Сохранить')
