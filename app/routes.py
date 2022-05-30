from datetime import datetime

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, NewGroupForm
from app.models import Users, Groups, Tests, Test_started


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Эмулятор КЕГЭ по информатике')


@app.route('/test/')
#@login_required
def test():
    return render_template('test.html', title='Эмулятор КЕГЭ по информатике')


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
    user = Users.query.filter_by(username=username).first_or_404()
    statuses = ('Неактивирован', 'Пользователь', 'Администратор', 'Ученик', 'Учитель', 'Родитель')
    role = statuses[user.role]
    return render_template('user.html', user=user, role=role)


@app.route('/edit_profile/<username>', methods=['GET', 'POST'])
@login_required
def edit_profile(username):
    usr = Users.query.filter_by(username=username).first_or_404()
    form = EditProfileForm()
    print(1)
    if form.validate_on_submit():
        usr.user_ = form.user_.data
        usr.role = form.role.data
        #usr.group_id = form.group.data
        db.session.commit()
        flash('Данные изменены')
        return redirect(url_for('adminpage'))
    elif request.method == 'GET':
        form.role.default = usr.role
        #form.group.default = usr.group_id
        form.process()
        form.user_.data = usr.user_
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
    '''if request.method == 'GET':
        gr = Groups.query.filter_by(group_id=group).first_or_404()
        usrs = Users.query.filter_by(group_id=group)
        return render_template('adminpage.html', title='Список группы '+gr.gr_name, usrs=usrs, groups=gr)'''
    usrs = Users.query.all()
    groups = Groups.query.all()
    return render_template('adminpage.html', title='Администрирование сайта', usrs=usrs, groups=groups)


@app.route('/newgroup', methods=['GET', 'POST'])
@login_required
def newgroup():
    form = NewGroupForm()
    if form.validate_on_submit():
        print(1)
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