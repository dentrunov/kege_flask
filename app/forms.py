from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, HiddenField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import *



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



