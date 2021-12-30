from flask import render_template, flash, redirect, url_for
from webapp import app
from webapp.forms import LoginForm
from config import Config
from flask_login import LoginManager, login_user, logout_user
from webapp.models import User 

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Alex'}
    return render_template('index.html', title='Home', user=user)

@app.route('/login')
def login():
    title = "Авторизация"
    login_form = LoginForm()
    return render_template('login.html', page_title=title, form=login_form)


@app.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Вы вошли на сайт')
            return redirect(url_for('index'))
    flash('Неправильное имя пользователя или пароль')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))