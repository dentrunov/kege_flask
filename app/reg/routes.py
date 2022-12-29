from flask import render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, reg, db, mail, CAPTCHA


import string
from random import choice

from app.reg.forms import *
from app.models import *
from app.email import *

def create_hash():
    return ''.join([choice(list(string.ascii_letters+string.digits)) for i in range(40)])

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
    return render_template('reg/login.html', title='Авторизация', form=form)


@app.route('/logout')
def logout():
    #выход пользователя
    logout_user()
    return redirect(url_for('index'))

@app.route('/forget_pwd', methods=['GET', 'POST'])
def forget_pwd():
    #форма отправки запроса восстановление пароля
    form = forgerPwdForm()
    if form.validate_on_submit():
        search = form.text.data
        usr = Users.query.filter((Users.username == search) | (Users.email == search)).first()
        if usr:
            #создание записи БД о запросе сброса пароля
            hsh = create_hash()
            rp = RestorePwd(user_id=usr.user_id, hash=hsh)
            db.session.add(rp)
            db.session.commit()
            #создание сообщения
            email_ = usr.email.split('@')
            em = email_[0][:2] + '*' * (len(email_[0]) - 2) + '@' + '*' * (len(email_[1]) - 4) + email_[1][-4:]
            #отправка письма
            subject = f'Сброс пароля на сайте {request.host}'
            recipients = [usr.email]
            text_body = render_template('reg/email/forget_pwd_email.txt', email=usr.email, hsh=hsh)
            html_body = render_template('reg/email/forget_pwd_email.html', email=usr.email, hsh=hsh)
            send_email(subject, recipients, text_body, html_body)
            flash(f'На электронную почту {em}, указанную в учетной записи, направлено сообщение'+ subject)
        else:
            flash('Пользователь не найден')
    return render_template('reg/forget_pwd.html', title='Восстановление пароля', form=form)

@app.route('/send_pwd/<hsh>', methods=['GET', 'POST'])
def send_pwd(hsh):
    #форма ввода нового пароля
    form = newPassForm()
    if form.validate_on_submit():
        hash_check = RestorePwd.query.filter_by(hash=hsh).first_or_404()
        usr = Users.query.filter_by(user_id=hash_check.user_id).first()
        usr.set_password(form.password.data)
        RestorePwd.query.filter_by(hash=hsh).delete()
        db.session.commit()
        return redirect('/reg.login')
    if request.method == 'GET':
        hash_check = RestorePwd.query.filter_by(hash=hsh).first_or_404()
        if hash_check:
            return render_template('reg/send_pwd.html', title='Восстановление пароля', form=form)
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
#функция регистрации
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    captcha = CAPTCHA.create()
    if form.validate_on_submit():
        c_hash = request.form.get('captcha-hash')
        c_text = request.form.get('captcha-text')
        if CAPTCHA.verify(c_text, c_hash):
            user = Users(username=form.username.data, email=form.email.data, user_=form.user_.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            # отправка письма
            subject = f'Вы зарегистрированы на сайте {request.host}'
            recipients = [form.email.data]
            text_body = render_template('reg/email/register_email.txt', username=form.user_.data)
            html_body = render_template('reg/email/register_email.html', username=form.user_.data)
            send_email(subject, recipients, text_body, html_body)
            flash('Поздравляем, вы зарегистрированы!')
            return redirect(url_for('login'))
        else:
            flash('Поздравляем, вы зарегистрированы!')
    return render_template('reg/register.html', title='Регистрация', form=form, captcha=captcha)




@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    #изменение профиля пользователя
    form = EditProfileForm()
    usr = Users.query.filter_by(user_id=current_user.user_id).first_or_404()
    if form.validate_on_submit():
        usr.user_ = form.user_.data
        usr.role = form.role.data
        #usr.parent_email = form.parent_email.data
        db.session.commit()
        flash('Данные изменены')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.user_.data = current_user.user_
        form.role.default = current_user.role
        #form.parent_email.data = current_user.parent_email
    return render_template('reg/edit_profile.html', title='Редактирование профиля', form=form)
