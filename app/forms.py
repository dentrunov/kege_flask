from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, HiddenField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import *



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

class EditUserInGroupForm(FlaskForm):
    groups_ = Groups.query.all()
    groups = SelectField('Выберите группу', choices=[(group.group_id, group.gr_name) for group in groups_])
    user = HiddenField()
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

class AddNewsForm(FlaskForm):
    news_title = TextAreaField('Название новости')
    news_text = TextAreaField('Текст новости')
    #TODO доделать выбор группы для новости
    submit = SubmitField('Сохранить')


class AddHWTaskForm(FlaskForm):
    HW_task_title = StringField('Название ДЗ')
    HW_task_text = TextAreaField('Содержание задания')
    HW_task_answer = StringField('Ответ')
    submit = SubmitField('Сохранить')

