from datetime import datetime
import json

from flask import render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import *
from app.models import Users, Groups, Tests, Test_started


@app.route('/')
@app.route('/index')
def index():
    tests = Tests.query.order_by(Tests.time_added.desc())
    return render_template('index.html', title='Эмулятор КЕГЭ по информатике', tests=tests)


@app.route('/test/<test>')
#@login_required
def test(test):
    # генерируем формы TODO перепроверить, 25 сделать не в списке
    answerSimpleForm = [AnswerSimpleForm() for i in range(1, 29)]
    answerTwoForm = [AnswerTwoForm() for i in range(1, 29)]
    answerManyForm = [AnswerManyForm() for i in range(1, 29)]
    #читаем задания теста из БД
    currentTest = Tests.query.filter_by(test_id=test).first_or_404()
    if not ('try' in session):
        #создаем новую записть прохождения теста
        newTest = Test_started(user_id=current_user.user_id, test_id=test)
        db.session.add(newTest)
        db.session.commit()
        #создаем сессию
        session['try'] = newTest.try_id
    else:
        #если тест уже начат TODO проверить проверку на завершенность
        #читаем данные начатого теста
        newTest = Test_started.query.filter_by(try_id=session['try']).first()
        for i in range(1,28):
            if getattr(newTest,'task_'+str(i)) is not None:
                if i in (17,18,20,26,27):
                    answerTwoForm[i].answerField1.data, answerTwoForm[i].answerField2.data = getattr(newTest, 'task_' + str(i)).split(';')
                elif i == 25:
                    field_full = getattr(newTest, 'task_' + str(i)).split(';')
                    for j in range(len(field_full)):
                        setattr(answerManyForm[i], 'answerField'+str(j)+'.data', field_full[j])
                else:
                    answerSimpleForm[i].answerField.data = getattr(newTest, 'task_'+str(i))

    #создаем рендер страницы
    testName = currentTest.test_name
    test_path = currentTest.path
    #записываем ответы на задания TODO пересмотреть этот момент
    test_tasks = [currentTest.task_1, currentTest.task_2, currentTest.task_3, currentTest.task_4, currentTest.task_5,
                  currentTest.task_6, currentTest.task_7, currentTest.task_8,currentTest.task_9, currentTest.task_10,
                  currentTest.task_11, currentTest.task_12, currentTest.task_13, currentTest.task_14, currentTest.task_15,
                  currentTest.task_16, currentTest.task_17, currentTest.task_18, currentTest.task_19, currentTest.task_20,
                  currentTest.task_21, currentTest.task_22, currentTest.task_23, currentTest.task_24, currentTest.task_25,
                  currentTest.task_26, currentTest.task_27]

    #генерируем рендер
    return render_template('test.html', title='Эмулятор КЕГЭ по информатике',
                           answerSimpleForm=answerSimpleForm, answerTwoForm=answerTwoForm,
                           answerManyForm=answerManyForm, test=testName, test_tasks=test_tasks, test_path=test_path)


@app.route('/taskcheck', methods=['POST'])
@login_required
def taskcheck():
    #скипт записи задания
    if request.method == "POST":
        task_number = request.form.get('answerNumber')
        if int(task_number) in (17, 18, 20, 26, 27):
            field = request.form.get('answerField1') + ';' + request.form.get('answerField2')
            print(field)
        elif int(task_number) == 25:
            field = ''
            for i in range(1, 11):
                if request.form.get('answerField' + str(i)) is not None:
                    field += (request.form.get('answerField' + str(i)) + ';')
                    print(field)
            field = field.rstrip(';')
        else:
            field = request.form.get('answerField')
        answer = Test_started.query.filter_by(try_id=session['try']).first()
        setattr(answer, 'task_'+task_number, field)
        db.session.commit()
        return json.dumps({'success': 'true', 'msg': 'Сохранено'})
    else:
        return json.dumps({'success': 'false', 'msg': 'Плохо'})


@app.route('/finishtest')
@login_required
def finishtest():
    #скрипт завершения теста пользователем
    if 'try' in session:
        pass
    else:
        pass


@app.route('/test1/')
#@login_required
#временная заглушка
def test1():
    answerSimpleForm = [AnswerSimpleForm(answerNumber=i) for i in range(1, 29)]
    answerTwoForm = [AnswerTwoForm(answerNumber=i) for i in range(1, 29)]
    answerManyForm = [AnswerManyForm(answerNumber=i) for i in range(1, 29)]

    return render_template('test.html', title='Эмулятор КЕГЭ по информатике',
                           answerSimpleForm=answerSimpleForm, answerTwoForm=answerTwoForm,
                           answerManyForm=answerManyForm)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неверный логин или пароль')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
#функция регистрации
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляем, вы зарегистрированы!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user_ = Users.query.filter_by(username=username).first_or_404()
    tests = Tests.query.order_by(Tests.time_added.desc())
    statuses = ('Неактивирован', 'Пользователь', 'Администратор', 'Ученик', 'Учитель', 'Родитель')
    role = statuses[user.role]
    return render_template('user.html', user=user_, role=role, tests=tests)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.user_ = form.user_.data
        current_user.role = form.role.data
        db.session.commit()
        flash('Данные изменены')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.user_.data = current_user.user_
        form.role.default = current_user.role
    return render_template('edit_profile.html', title='Редактирование профиля', form=form)


@app.route('/adminpage_groups/<group>')
@login_required
def adminpage_groups(group):
    gr = Groups.query.filter_by(group_id=group).first_or_404()
    usrs = Users.query.filter_by(group_id=group)
    return render_template('adminpage_groups.html', title='Список группы '+gr.gr_name, usrs=usrs, group=gr)



@app.route('/adminpage')
@login_required
def adminpage():
    usrs = Users.query.all()
    groups = Groups.query.all()
    return render_template('adminpage.html', title='Администрирование сайта', usrs=usrs, groups=groups)


@app.route('/adminpage_newtest', methods=['GET', 'POST'])
@login_required
def adminpage_newtest():
    form = AddNewTest()
    tests = Tests.query.all()
    if form.validate_on_submit():
        new_test = Tests(user_id=current_user.user_id,
                         path=form.pathField.data,
                         test_name=form.testnameField.data,
                         task_1=form.task_Field1.data, task_2=form.task_Field2.data, task_3=form.task_Field3.data,
                         task_4=form.task_Field4.data, task_5=form.task_Field5.data, task_6=form.task_Field6.data,
                         task_7=form.task_Field7.data, task_8=form.task_Field8.data, task_9=form.task_Field9.data,
                         task_10=form.task_Field10.data, task_11=form.task_Field11.data, task_12=form.task_Field12.data,
                         task_13=form.task_Field13.data, task_14=form.task_Field14.data, task_15=form.task_Field15.data,
                         task_16=form.task_Field16.data, task_17=form.task_Field17.data, task_18=form.task_Field18.data,
                         task_19=form.task_Field19.data, task_20=form.task_Field20.data, task_21=form.task_Field21.data,
                         task_22=form.task_Field22.data, task_23=form.task_Field23.data, task_24=form.task_Field24.data,
                         task_25=form.task_Field25.data, task_26=form.task_Field26.data, task_27=form.task_Field27.data)
        db.session.add(new_test)
        db.session.commit()
        flash('Тест сохранен')
        return redirect(url_for('adminpage_newtest'))
    elif request.method == 'GET':
        print(1)
    return render_template('adminpage_newtest.html', title='Добавление теста', form=form, tests=tests)


@app.route('/adminpage_edit_user/<username>', methods=['GET', 'POST'])
@login_required
def adminpage_edit_user(username):
    usr = Users.query.filter_by(username=username).first_or_404()
    form = EditAdminUserProfileForm()
    if form.validate_on_submit():
        usr.user_ = form.user_.data
        usr.role = form.role.data
        usr.group_id = form.group.data
        db.session.commit()
        flash('Данные изменены')
        return redirect(url_for('adminpage'))
    elif request.method == 'GET':
        form.role.default = usr.role
        form.group.default = usr.group_id
        form.process()
        form.user_.data = usr.user_
    return render_template('adminpage_edit_user.html', title='Редактирование профиля', form=form)


@app.route('/newgroup', methods=['GET', 'POST'])
@login_required
def newgroup():
    form = NewGroupForm()
    if form.validate_on_submit():
        group = Groups(gr_name=form.gr_name.data, stud_year=form.stud_year.data)
        db.session.add(group)
        db.session.commit()
        flash('Данные изменены')
        return redirect(url_for('adminpage'))
    elif request.method == 'GET':
        pass
    return render_template('newgroup.html', title='Добавление группы', form=form)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_visit_time = datetime.now()
        db.session.commit()