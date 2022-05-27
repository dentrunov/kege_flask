from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/test/')
def test():
    return render_template('test.html')
'''
@app.route('/login')
def login():
    form = LoginForm()'''


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Авторизация для пользователя {}, запомнить меня={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Авторизация', form=form)