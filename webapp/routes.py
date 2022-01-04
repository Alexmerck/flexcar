from flask import render_template, flash, redirect, url_for, request
from webapp import app
from webapp.forms import LoginForm
from webapp.config import Config
from flask_login import LoginManager, login_user, logout_user
from webapp.models import User 
from webapp.forms import CarinputForm
from webapp import db
from webapp.models import Vehicle



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


@app.route('/carinput', methods=["POST"])
def process_сarinput():
    form = CarinputForm()
    if form.validate_on_submit():
        car =  Vehicle(
            title=form.title.data, 
            manufacturer=form.manufacturer.data, 
            model=form.model.data, 
            production_year=form.production_year.data,
            engine_type=form.engine_type.data,
            volume=form.volume.data,
            transmission_type=form.transmission_type.data,
            body=form.body.data
            )
        db.session.add(car)
        db.session.commit()
        
        return redirect(url_for('usercar'))

