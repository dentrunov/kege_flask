from datetime import datetime, time
import json

from flask import render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import *
from app.models import *


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Эмулятор КЕГЭ по информатике')


@app.route('/test/<test>')
#@login_required
def test(test):
    # генерируем формы TODO перепроверить, 25 сделать не в списке
    answerSimpleForm = [AnswerSimpleForm() for i in range(1, 29)]
    answerTwoForm = [AnswerTwoForm() for i in range(1, 29)]
    answerManyForm = [AnswerManyForm() for i in range(1, 29)]
    #читаем задания теста из БД
    currentTest = Tests.query.filter_by(test_id=test).first_or_404()
    #t = 1000
    t = 235*60
    if not ('try' in session):
        #создаем новую записть прохождения теста
        newTest = Test_started(user_id=current_user.user_id, test_id=test,test_name=currentTest.test_name)
        db.session.add(newTest)
        db.session.commit()
        #создаем сессию
        session['try'] = newTest.try_id
        #работа с таймером - стартуем полный таймер
        time_left = time(t//60//60, t//60%60, t%60)
    else:
        #если тест уже начат
        #читаем данные начатого теста
        newTest = Test_started.query.filter_by(try_id=session['try']).first()
        #работа с таймером - вычисляем оставшееся время
        t1 = t - newTest.time_left
        time_left = time(t1//60//60, t1//60%60, t1%60)
        # создание форм для заданий, заполнение уже данными ответами
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
    test_tasks = tuple([getattr(currentTest, 'task_'+str(i)) for i in range (1,28)])
    #оставлю для истории)
    '''test_tasks = (currentTest.task_1, currentTest.task_2, currentTest.task_3, currentTest.task_4, currentTest.task_5,
                  currentTest.task_6, currentTest.task_7, currentTest.task_8,currentTest.task_9, currentTest.task_10,
                  currentTest.task_11, currentTest.task_12, currentTest.task_13, currentTest.task_14, currentTest.task_15,
                  currentTest.task_16, currentTest.task_17, currentTest.task_18, currentTest.task_19, currentTest.task_20,
                  currentTest.task_21, currentTest.task_22, currentTest.task_23, currentTest.task_24, currentTest.task_25,
                  currentTest.task_26, currentTest.task_27)'''

    #генерируем рендер
    return render_template('test.html', title='Эмулятор КЕГЭ по информатике',
                           answerSimpleForm=answerSimpleForm, answerTwoForm=answerTwoForm,
                           answerManyForm=answerManyForm, test=testName, test_tasks=test_tasks, test_path=test_path, time_left=time_left)


@app.route('/taskcheck', methods=['POST'])
@login_required
def taskcheck():
    #скипт записи задания
    if request.method == "POST":
        #запрос номера задания
        task_number = request.form.get('answerNumber')
        #проверка заданий с несколькими ответами
        if int(task_number) in (17, 18, 20, 26, 27):
            field = request.form.get('answerField1') + ';' + request.form.get('answerField2')
        elif int(task_number) == 25:
            field = ''
            for i in range(1, 11):
                if request.form.get('answerField' + str(i)) is not None:
                    field += (request.form.get('answerField' + str(i)) + ';')
            field = field.rstrip(';')
        else:
            field = request.form.get('answerField')
        #запись ответа и времени записи ответа в БД
        answer = Test_started.query.filter_by(try_id=session['try']).first()
        setattr(answer, 'task_'+task_number, field)
        delta = datetime.now() - answer.time_start
        answer.time_left = int(delta.seconds)
        db.session.commit()
        return json.dumps({'success': 'true', 'msg': 'Сохранено'})
    else:
        return json.dumps({'success': 'false', 'msg': 'Ошибка сохранения, обратитесь к администратору'})


@app.route('/showresult/<try_id>')
@login_required
def showresult(try_id):
    if 'try' in session:
        session.pop('try')
    #TODO Вот тут доделать с JOIN и вообще пересмотреть весь скрипт и вью
    #запрос заданий теста
    currentTry = Test_started.query.filter_by(try_id=try_id).first_or_404()
    currentAnswers = tuple([getattr(currentTry, 'task_' + str(i)) for i in range(1, 28)])

    test = currentTry.test_id
    #запрос ответов теста
    currentTest = Tests.query.filter_by(test_id=test).first_or_404()
    curTest = tuple([getattr(currentTest, 'task_' + str(i)) for i in range(1, 28)])
    #проверка заданий теста, если он не проверен
    if currentTry.primary_mark == 0:
        summ = 0
        for i in range(len(currentAnswers)):
            if curTest[i] == currentAnswers[i]:
                summ += 1
        #разбалловка первичного балла и запись в БД TODO вынести в глобальные переменные
        marks = (0, 4, 14, 20, 27, 34, 40, 43, 45, 48, 50, 53, 55, 58, 60, 63, 65, 68, 70, 73, 75, 78, 80, 83, 85, 88, 90, 93, 95, 100)
        mark = {i: m for i, m in enumerate(marks)}
        m = mark[summ]
        currentTry.primary_mark = summ
        currentTry.final_mark = m
        db.session.commit()

    else:
        summ = currentTry.primary_mark
        m = currentTry.final_mark
    test_name = currentTry.test_name
    #TODO и всё-таки оптимизировать этот запрос c JOIN
    #запрос имени пользователя
    cur_user = Users.query.filter_by(user_id=currentTry.user_id).first_or_404()
    usr = cur_user.user_
    return render_template('showresult.html', title='Результаты теста '+currentTest.test_name+' '+currentTry.time_end.strftime('%d.%m.%Y'),
                           currentAnswers=currentAnswers, test=curTest, summ=summ, mark=m, test_name=test_name, usr=usr)


@app.route('/test_list')
@login_required
def test_list():
    #просмотр тестов
    tests = Tests.query.order_by(Tests.time_added.desc()).limit(10)
    test_not_done = Test_started.query.filter_by(user_id=current_user.user_id, time_end=None).order_by(Test_started.time_start.desc())
    tests_done = Test_started.query.filter(Test_started.user_id == current_user.user_id, Test_started.time_end != None).order_by(Test_started.time_start.desc())
    return render_template('test_list.html', title='Выбор варианта КЕГЭ по информатике',
                           tests=tests,tests_not_done=test_not_done, tests_done=tests_done)

@app.route('/test_continue/<test_id>')
@login_required
def test_continue(test_id):
    #продолжение незавершенного теста TODO что-то со временем - пофиксить
    test = Test_started.query.filter_by(try_id=test_id).first()
    session['try'] = test.try_id
    return render_template('test_continue.html', title='Вы хотите продолжить тест', test=test.test_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    #авторизация
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
    #выход пользователя
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
    #просмотр пользователя, TODO возможно, сделать JOIN
    user_ = Users.query.filter_by(username=username).first_or_404()
    tests = Tests.query.order_by(Tests.time_added.desc()).all()
    statuses = ('Неактивирован', 'Пользователь', 'Администратор', 'Ученик', 'Учитель', 'Родитель')
    role = statuses[user_.role]
    if current_user.role in (2,4):
        groups = Groups.query.all()
        users = Users.query.filter_by(group_id=1, role=3).all()
        admin_users_info = {'groups':groups, 'users':users}
    else:
        admin_users_info = (None,)
    return render_template('user.html', user=user_, role=role, tests=tests, admin_users_info=admin_users_info)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    #изменение профиля пользователя
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.user_ = form.user_.data
        current_user.role = form.role.data
        current_user.parent_email = form.parent_email.data
        db.session.commit()
        flash('Данные изменены')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.user_.data = current_user.user_
        form.role.default = current_user.role
        form.parent_email.data = current_user.parent_email
    return render_template('edit_profile.html', title='Редактирование профиля', form=form)


@app.route('/adminpage_groups/<group>')
@login_required
def adminpage_groups(group):
    #админский просмотр групп TODO сделать формы добавления
    users = Users.query.filter_by(group_id=group).order_by(Users.user_.asc()).join(Groups,
                                                                                Groups.group_id == group).add_columns(
        Groups.group_id, Groups.gr_name, Users.username, Users.user_).all()
    return render_template('showgroup.html', title='Список группы {}'.format(users[0].gr_name), users=users)


@app.route('/adminpage')
@login_required
def adminpage():
    #административная страница
    usrs = Users.query.order_by(Users.user_.asc()).all()
    groups = Groups.query.order_by(Groups.gr_name.asc()).all()
    tests = Tests.query.order_by(Tests.time_added.desc()).all()
    return render_template('adminpage.html', title='Администрирование сайта', usrs=usrs, groups=groups, tests=tests)



@app.route('/adminpage_newtest', methods=['GET', 'POST'])
@login_required
def adminpage_newtest():
    #создание нового теста из картинок TODO сделать библиотеку заданий и тд
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
        return redirect(url_for('adminpage'))
    elif request.method == 'GET':
        pass
    return render_template('adminpage_newtest.html', title='Добавление теста', form=form, tests=tests)

@app.route('/adminpage_configtest/<t_id>', methods=['GET', 'POST'])
@login_required
def adminpage_configtest(t_id):
    #изменение нового теста
    test = Tests.query.filter_by(test_id=t_id).first_or_404()
    form = AddNewTest()
    if form.validate_on_submit():
        test.path=form.pathField.data; test.test_name=form.testnameField.data; test.task_1=form.task_Field1.data
        test.task_2=form.task_Field2.data; test.task_3=form.task_Field3.data; test.task_4=form.task_Field4.data
        test.task_5=form.task_Field5.data; test.task_6=form.task_Field6.data; test.task_7=form.task_Field7.data
        test.task_8=form.task_Field8.data; test.task_9=form.task_Field9.data; test.task_10=form.task_Field10.data
        test.task_11=form.task_Field11.data; test.task_12=form.task_Field12.data; test.task_13=form.task_Field13.data
        test.task_14=form.task_Field14.data; test.task_15=form.task_Field15.data; test.task_16=form.task_Field16.data
        test.task_17=form.task_Field17.data; test.task_18=form.task_Field18.data; test.task_19=form.task_Field19.data
        test.task_20=form.task_Field20.data; test.task_21=form.task_Field21.data; test.task_22=form.task_Field22.data
        test.task_23=form.task_Field23.data; test.task_24=form.task_Field24.data; test.task_25=form.task_Field25.data
        test.task_26=form.task_Field26.data; test.task_27=form.task_Field27.data
        db.session.add(test)
        db.session.commit()
        flash('Тест сохранен')
        return redirect(url_for('adminpage'))
    else:
        form.pathField.data = test.path; form.testnameField.data = test.test_name
        form.task_Field1.data = test.task_1; form.task_Field2.data = test.task_2; form.task_Field3.data = test.task_3; form.task_Field4.data = test.task_4
        form.task_Field5.data = test.task_5; form.task_Field6.data = test.task_6; form.task_Field7.data = test.task_7; form.task_Field8.data = test.task_8
        form.task_Field9.data = test.task_9; form.task_Field10.data = test.task_10; form.task_Field11.data = test.task_11; form.task_Field12.data = test.task_12
        form.task_Field13.data = test.task_13; form.task_Field14.data = test.task_14; form.task_Field15.data = test.task_15; form.task_Field16.data = test.task_16
        form.task_Field17.data = test.task_17; form.task_Field18.data = test.task_18; form.task_Field19.data = test.task_19; form.task_Field20.data = test.task_20
        form.task_Field21.data = test.task_21; form.task_Field22.data = test.task_22; form.task_Field23.data = test.task_23; form.task_Field24.data = test.task_24
        form.task_Field25.data = test.task_25; form.task_Field26.data = test.task_26; form.task_Field27.data = test.task_27
    return render_template('adminpage_edit.html', title='Изменение теста', form=form)

@app.route('/adminpage_edit_user/<username>', methods=['GET', 'POST'])
@login_required
def adminpage_edit_user(username):
    #изменение пользователя админом
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
    #создание новой группы
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

@app.route('/showgroup/<gr>')
@login_required
def showgroup(gr):
    #страница просмотра списка группы (результаты тестов)
    users = Users.query.filter_by(group_id=gr).order_by(Users.user_.asc()).join(Groups, Groups.group_id == gr).add_columns(Groups.group_id, Groups.gr_name, Users.username, Users.user_).all()
    return render_template('showgroup.html', title='Список группы {}'.format(users[0].gr_name), users=users)

@app.route('/showuser_result/<usr>')
@login_required
def showuser_result(usr):
    #страница просмотра списка теста пользователя TODO переписать с JOIN
    user_ = Users.query.filter_by(username=usr).first_or_404()
    user_tests = Test_started.query.filter_by(user_id=user_.user_id).order_by(Test_started.time_end.desc()).all()
    return render_template('showuser.html', title='Список тестов пользователя {}'.format(user_.user_), usr=user_, tests=user_tests)

@app.route('/showtest_allusers/<test>')
@login_required
def showtest_allusers(test):
    #просмотр пользователей по тесту TODO сделать пагинацию (пока не получается)
    current_test = Test_started.query.filter_by(test_id=test).order_by(Test_started.time_end.desc()).join(Users, Users.user_id==Test_started.user_id).add_columns(Users.user_, Users.username, Test_started.try_id,
                                                                                                                           Test_started.test_name, Test_started.time_end, Test_started.primary_mark, Test_started.final_mark)
    #page = request.args.get('page', 1,  type=int)
    #current_test = Test_started.query.filter_by(test_id=test).paginate(page, app.config['POSTS_PER_PAGE'], False).order_by(Test_started.time_end.desc()).join(Users,
    #                                                                                                     Users.user_id == Test_started.user_id).add_columns(
    #    Users.user_, Users.username, Test_started.try_id,
    #    Test_started.test_name, Test_started.time_end, Test_started.primary_mark, Test_started.final_mark)
    return render_template('showtest.html', title='Список пользователей, выполнивших тест', tests=current_test)

@app.route('/admin_result')
@login_required
def admin_result():
    #временная страница обзора БД
    test_e = Test_started().query.all()
    return render_template('admin_result.html',test_e=test_e)



@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_visit_time = datetime.now()
        db.session.commit()


@app.route('/finishtest')
@login_required
def finishtest():
    #скрипт завершения теста пользователем
    if 'try' in session:
        try_ = session['try']        #доделать с join
        currentTry = Test_started.query.filter_by(try_id=try_).first_or_404()
        currentTry.ended = True
        currentTry.time_end = datetime.now()
        db.session.commit()
        return json.dumps({'success': 'true', 'msg': try_})

    else:
        return redirect(url_for('test_list'))

@app.route('/lessons', methods=['POST', 'GET'])
def lessons():
    #список видео
    less = Videos.query.all()
    return render_template('lessons.html',title='Обучающие видео', lessons=less)


@app.route('/adminpage_addvideo', methods=['POST', 'GET'])
def adminpage_addvideo():
    form = AddVideoForm()
    if form.validate_on_submit():
        video = Videos(v_link=form.video_link.data, v_name=form.video_name.data, v_text=form.video_text.data)
        db.session.add(video)
        db.session.commit()
        flash('Видео сохранено')
        return redirect(url_for('adminpage'))
    return render_template('adminpage_addvideo.html', title='Добавление видео', form=form)