from flask import render_template, flash, redirect, url_for, request
from flask_login.utils import login_required
from webapp import app, db
from webapp.forms import LoginForm, Signup
from config import Config
from flask_login import LoginManager, login_user, logout_user, current_user
from webapp.models import User 
from webapp.forms import CarinputForm
from getpass import getpass


@app.route('/')
@app.route('/index')
@login_required
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

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
       return redirect(url_for('index'))
    form = Signup()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляем, вы успешно зарегистрировались')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Signup', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/usercars')
def usercar():
    user = {'username': 'testuser'}
    carlist =[
        {'manufacturer': 'BMW',
        'model':'X1'},
        {'manufacturer': 'ff',
        'model':'X176'},
        {'manufacturer': 'deawoo',
        'model':'1'}
        ]
    return render_template('usercars.html', title = 'GARAGE', user = user, carlist = carlist)


@app.route('/carinput')
def сarinput():
    title = "Добавление авто в гараж"
    сarinput_form = CarinputForm()
    return render_template('carinput.html', page_title=title, form=сarinput_form)
