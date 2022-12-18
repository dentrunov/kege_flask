from flask import render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, reg, db, mail

import json

from app.admin.forms import *
from app.models import *
from app.email import *

@app.route('/adminpage_groups/<group>')
@login_required
def adminpage_groups(group):
    #админский просмотр групп TODO сделать формы добавления
    users = Users.query.filter_by(group_id=group).order_by(Users.user_.asc()).join(Groups,
                                                                                Groups.group_id == group).add_columns(
        Groups.group_id, Groups.gr_name, Users.username, Users.user_).all()
    forms = [EditUserInGroupForm() for i in range(len(users))]
    if len(users) > 0:
        gr_name = users[0].gr_name
    else:
        gr_name = group #TODO доделать название группы
    return render_template('admin/adminpage_groups.html', title='Список группы {}'.format(gr_name), users=users, gr_name=gr_name, forms=forms)

@app.route('/changegroup', methods=['POST'])
@login_required
def changegroup():
    #скрипт изменения группы пользователя
    if request.method == "POST":
        username = request.form.get('user')
        group = request.form.get('groups')
        usr = Users.query.filter_by(username=username).first_or_404()
        usr.group_id = group
        db.session.commit()
        return json.dumps({'success': 'true', 'msg': 'Сохранено'})
    else:
        return json.dumps({'success': 'false', 'msg': 'Ошибка сохранения, обратитесь к администратору'})

@app.route('/adminpage')
@login_required
def adminpage():
    #административная страница
    usrs = Users.query.order_by(Users.user_.asc()).all()
    groups = Groups.query.order_by(Groups.gr_name.asc()).all()
    tests = Tests.query.order_by(Tests.time_added.desc()).all()
    return render_template('admin/adminpage.html', title='Администрирование сайта', usrs=usrs, groups=groups, tests=tests)


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
    return render_template('admin/adminpage_newtest.html', title='Добавление теста', form=form, tests=tests)

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
    return render_template('admin/adminpage_edit.html', title='Изменение теста', form=form)


@app.route('/adminpage_delete_test', methods=['POST'])
@login_required
def adminpage_delete_test():
    #скрипт удаления тестов
    if request.method == 'POST':
        #TODO доделать алерт красиво
        t_id = request.json['t_id']
        test = Tests.query.filter_by(test_id=t_id).delete()
        db.session.commit()
        return json.dumps({'success': 'true', 'msg': 'Сохранено'})
    else:
        return json.dumps({'success': 'false', 'msg': 'Ошибка сохранения, обратитесь к администратору'})



@app.route('/adminpage_hide_test', methods=['POST'])
@login_required
def adminpage_hide_test():
    # скрипт сокрытия/показа тестов
    if request.method == 'POST':
        #TODO доделать алерт красиво
        t_id = request.json['t_id']
        test = Tests.query.filter_by(test_id=t_id).first_or_404()
        test.test_hidden = not(test.test_hidden)
        db.session.commit()
        return json.dumps({'success': 'true', 'msg': 'Сохранено'})
    else:
        return json.dumps({'success': 'false', 'msg': 'Ошибка сохранения, обратитесь к администратору'})

@app.route('/admin_result')
@login_required
def admin_result():
    #временная страница обзора БД
    test_e = Test_started().query.all()
    return render_template('admin/admin_result.html',test_e=test_e)

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
    return render_template('admin/adminpage_edit_user.html', title='Редактирование профиля', usr=usr, form=form)


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
    return render_template('admin/newgroup.html', title='Добавление группы', form=form)

@app.route('/showgroup/<gr>')
@login_required
def showgroup(gr):
    #страница просмотра списка группы (результаты тестов)
    #users = Users.query.filter_by(group_id=gr).order_by(Users.user_.asc()).join(Groups, Groups.group_id == gr).add_columns(Groups.group_id, Groups.gr_name, Users.username, Users.user_).all()
    users = Users.query.filter_by(group_id=gr).order_by(Users.user_.asc()).all()
    users_list = [user.user_id for user in users]
    group = Groups.query.filter_by(group_id=gr).first()
    tests = Tests.query.order_by(Tests.time_added).all()
    tests_done = Test_started().query.filter(Test_started.ended==True and Test_started.user_id in users_list).order_by(Test_started.user_id.asc()).all()
    users_list_with_tests = {usr: {test.test_id: (test.primary_mark, test.final_mark) for test in tests_done if test.user_id==usr} for usr in users_list}
    gr_name = group.gr_name
    return render_template('admin/showgroup.html', title='Список группы {}'.format(gr_name), users=users, gr_name=gr_name, tests=tests, all_tests=users_list_with_tests)


@app.route('/adminpage_addvideo', methods=['POST', 'GET'])
@login_required
def adminpage_addvideo():
    form = AddVideoForm()
    if form.validate_on_submit():
        video = Videos(v_link=form.video_link.data, v_name=form.video_name.data, v_text=form.video_text.data)
        db.session.add(video)
        db.session.commit()
        flash('Видео сохранено')
        return redirect(url_for('adminpage'))
    return render_template('admin/adminpage_addvideo.html', title='Добавление видео', form=form)

@app.route('/adminpage_addnews', methods=['POST', 'GET'])
@login_required
def adminpage_addnews():
    form = AddNewsForm()
    if form.validate_on_submit():
        news = News_all(news_title=form.news_title.data, news_text=form.news_text.data)
        db.session.add(news)
        db.session.commit()
        flash('Новость сохранена')
        return redirect(url_for('adminpage'))
    return render_template('admin/adminpage_addnews.html', title='Добавление видео', form=form)


@app.route('/homeworks_addtask', methods=['POST', 'GET'])
@login_required
def homeworks_addtask():
    form = AddHWTaskForm()
    if form.validate_on_submit():
        hw_task = HW_tasks(
            task_text=form.HW_task_text.data,
            task_answer=form.HW_task_answer.data)
        return redirect(url_for('adminpage'))
    return render_template('admin/homeworks_addtask.html', title='Добавление задания')

@app.route('/homeworks_addhw', methods=['POST', 'GET'])
@login_required
def homeworks_addhomework():
    #создание домашнего задания
    pass