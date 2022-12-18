import string
from random import choice
from datetime import datetime, time
import json

from flask import render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
#from sqlalchemy import or_

from app import app, db, mail, CAPTCHA
from app.forms import *
from app.models import *
from app.email import *



def marking(x):
    #функция возвращает итоговый балл по первичному
    marks = (0, 4, 14, 20, 27, 34, 40, 43, 45, 48, 50, 53, 55, 58, 60, 63, 65, 68, 70, 73, 75, 78, 80, 83, 85, 88, 90, 93, 95, 100)
    mark = {i: m for i, m in enumerate(marks)}
    return mark[x]

@app.route('/')
@app.route('/index')
def index():
    news = News_all.query.filter_by(news_show_group=0).order_by(News_all.new_date.desc()).limit(4)
    return render_template('index.html', title='Эмулятор КЕГЭ по информатике', news=news)


@app.route('/test/<test>')
@login_required
def test(test):
    #TODO если пользователь завершил тест

    #генерируем формы TODO перепроверить
    answerSimpleForm = [AnswerSimpleForm() for i in range(1, 29)]
    answerTwoForm = [AnswerTwoForm() for i in range(1, 29)]
    answerManyForm_25 = AnswerManyForm()
    #читаем задания теста из БД
    currentTest = Tests.query.filter_by(test_id=test).first_or_404()
    task_25_l = len(currentTest.task_25.split(';'))
    #t = 1000
    #установка времени в минутах
    t = 235*60
    if not ('try' in session):
        #создаем новую записть прохождения теста
        newTest = Test_started(user_id=current_user.user_id, test_id=test,test_name=currentTest.test_name, path=currentTest.path)
        db.session.add(newTest)
        #изменяем количество решений
        currentTest.test_starts_number = currentTest.test_starts_number + 1
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
                    field_full = newTest.task_25.split(';')
                    task_25_len = len(field_full)
                    for j in range(task_25_len):
                        setattr(answerManyForm_25, 'answerField' + str(j) + '.data', field_full[j])
                    else:
                        task_25_len = 0
                else:
                    answerSimpleForm[i].answerField.data = getattr(newTest, 'task_'+str(i))


    #создаем рендер страницы
    testName = currentTest.test_name
    test_path = currentTest.path
    #записываем ответы на задания
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
                           answerManyForm=answerManyForm_25, test=testName, test_tasks=test_tasks, task_25_len=task_25_l, test_path=test_path, time_left=time_left)


@app.route('/taskcheck', methods=['POST'])
@login_required
def taskcheck():
    #скипт записи задания
    if request.method == "POST":
        #запрос номера задания
        task_number = request.form.get('answerNumber')
        #проверка заданий с несколькими ответами
        if int(task_number) in (17, 18, 20, 26, 27):
            field = request.form.get('answerField1').strip() + ';' + request.form.get('answerField2').strip()
        elif int(task_number) == 25:
            field = ''
            for i in range(1, 11):
                if request.form.get('answerField' + str(i)) is not None:
                    field += (request.form.get('answerField' + str(i)).strip() + ';')
            field = field.rstrip(';')
        else:
            field = request.form.get('answerField').strip()
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
    #запрос заданий теста
    currentTry = Test_started.query.filter_by(try_id=try_id).first_or_404()
    currentAnswers = tuple([getattr(currentTry, 'task_' + str(i)) for i in range(1, 28)])

    test = currentTry.test_id
    #запрос ответов теста
    currentTest = Tests.query.filter_by(test_id=test).first_or_404()
    curTest = tuple([getattr(currentTest, 'task_' + str(i)) for i in range(1, 28)])
    #проверка заданий теста, если он не проверен
    summ = currentTry.primary_mark
    m = currentTry.final_mark
    if currentTry.primary_mark == 0:
        summ = 0
        for i in range(len(currentAnswers)):
            if i in (25,26):
                if currentAnswers[i] != None and curTest[i] != None:
                    curT = curTest[i].split(';')
                    curA = currentAnswers[i].split(';')
                    if len(curT) > 1:
                        for j in range(2):
                            summ += curT[j] == curA[j]
            else:
                summ += curTest[i] == currentAnswers[i]
        #разбалловка первичного балла и запись в БД
        m = marking(summ)
        currentTry.primary_mark = summ
        currentTry.final_mark = m

    if currentTest.test_avg_result == 0:
        #вычисление среднего балла
        test_trys = Test_started.query.filter_by(test_id=test).all()
        avg = [x.primary_mark for x in test_trys]
        avg_mark = sum(avg) / len(avg)
        currentTest.test_avg_result = avg_mark
    else:
        summ = currentTry.primary_mark
        m = currentTry.final_mark
    db.session.commit()
    test_name = currentTry.test_name
    #TODO и всё-таки оптимизировать этот запрос c JOIN
    #запрос имени пользователя
    cur_user = Users.query.filter_by(user_id=currentTry.user_id).first_or_404()
    usr = cur_user.user_
    return render_template('showresult.html', title='Результаты теста '+currentTest.test_name+' '+currentTry.time_start.strftime('%d.%m.%Y'),
                           currentAnswers=currentAnswers, test=curTest, summ=summ, mark=m, test_name=test_name, usr=usr)


@app.route('/test_list')
@login_required
def test_list():
    #просмотр тестов
    tests = Tests.query.filter_by(test_hidden=True).order_by(Tests.time_added.desc()).limit(10)
    x = 0
    #TODO переделать, какая-то фигня
    for t in tests:
        x += 1
    if x == 0:
        tests = None
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
    return render_template('user.html', title=f'Личный кабинет пользователя {user_.user_}', user=user_, role=role, tests=tests, admin_users_info=admin_users_info)


@app.route('/showuser_result/<usr>')
@login_required
def showuser_result(usr):
    #страница просмотра списка теста пользователя TODO переписать с JOIN
    user_ = Users.query.filter_by(username=usr).first_or_404()
    user_tests = Test_started.query.filter_by(user_id=user_.user_id).order_by(Test_started.try_id.desc()).all()
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
        currentTry = Test_started.query.filter_by(try_id=try_).first_or_404()
        #msg = Message("Тестовое сообщение", recipients=[current_user.email])
        subject = f'Тест {currentTry.test_name} завершен'
        recipients = [current_user.email]
        if current_user.parent_email is not None:
            recipients += [current_user.parent_email]
        text_body = render_template('reg/email/end_test.txt', tr=currentTry)
        html_body = render_template('reg/email/end_test.html', tr=currentTry)
        send_email(subject, recipients, text_body, html_body)
        #TODO отправляется, попоадает в спам, доделать верстку
        return json.dumps({'success': 'true', 'msg': try_})

    else:
        return redirect(url_for('test_list'))

@app.route('/lessons', methods=['POST', 'GET'])
def lessons():
    #список видео
    less = Videos.query.all()
    return render_template('lessons.html',title='Обучающие видео', lessons=less)


@app.route('/homeworks_show', methods=['POST', 'GET'])
@login_required
def homeworks_show():
    #просмотр домашних заданий TODO сделать выборку по пользователю для ученика
    homeworks = Homeworks.query().filter_by(hw_user_id=current_user.user_id).order_by(Homeworks.hw_test_date.desc).limit(10)
    return render_template('showhomeworks.html', title='Домашние задания', homeworks=homeworks)


@app.route('/hometasks_show/<task>')
@login_required
def hometasks_show(task):
    # просмотр всех отдельных заданий
    if task == 'all':
        #TODO потом сделать выбор предмета
        themes = Themes.query().filter_by(theme_subject=1).order_by(Themes.theme_number.asc).all_or_404()
        t_name = 'информатике'
        return render_template('showhometasks.html', title='Задания по темам ЕГЭ по '+ t_name, themes=themes)
    else:
        tasks = HW_tasks.query().filter_by(task_number=task).order_by(HW_tasks.task_id.desc).all_or_404()
        return render_template('showtask.html', title='Задания по теме' + str(task), tasks=tasks)


