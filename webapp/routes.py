from flask import render_template, flash, redirect, url_for, request
from flask_login.utils import login_required
from webapp import app, db
from webapp.forms import LoginForm, Signup
from flask_login import LoginManager, login_user, logout_user, current_user
from webapp.models import User 
from webapp.forms import CarinputForm
from getpass import getpass
from sqlalchemy.orm import selectinload
from webapp import app
from webapp.forms import LoginForm
from config import Config
from webapp.models import User 
from webapp.forms import CarinputForm
from webapp import db
from webapp.models import Vehicle
from webapp.forms import ManufacturerForm, Car_base



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
    # in this rout used only test data, in future it should be changed on real data from db table Vehicle
    # start
    user = {'username': 'testuser'}
    carlist = [
        {'manufacturer': 'BMW',
        'model': 'X1'},
        {'manufacturer': 'ff',
        'model': 'X176'},
        {'manufacturer': 'deawoo',
        'model': '1'}
        ]
    # end
    return render_template(
        'usercars.html', title='GARAGE', user=user, carlist=carlist
        )


@app.route('/get_manufacturer')
def get_manufacturer():
    form = ManufacturerForm()
    return render_template('get_manufacturer.html', title="заполнение поля производителя автомобиля", form=form)


@app.route('/process_get_manufacturer', methods=["POST"])
def process_get_manufacturer():
    form = ManufacturerForm()
    if form.validate_on_submit():
        manufacturer = form.manufacturer.data
        title = "Добавление авто в гараж"
        сarinput_form = CarinputForm()
        сarinput_form.manufacturer.default = manufacturer
        return render_template(
            'carinput.html', page_title=title, form=сarinput_form
        )


@app.route('/process_carinput', methods=['POST'])
def process_сarinput():
    сarinput_form = CarinputForm()
    if сarinput_form.validate_on_submit():
        car = Vehicle(
            title=сarinput_form.title.data,
            manufacturer=сarinput_form.manufacturer.data,
            model=сarinput_form.model.data,
            production_year=сarinput_form.production_year.data,
            engine_type=сarinput_form.engine_type.data,
            volume=сarinput_form.volume.data,
            transmission_type=сarinput_form.transmission_type.data,
            body=сarinput_form.body.data
        )
        db.session.add(car)
        db.session.commit()
        return redirect(url_for('usercar'))
