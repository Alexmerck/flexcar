from flask import render_template, flash, redirect, url_for, request
from sqlalchemy.orm import selectinload
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


from webapp.forms import ManufacturerForm, Car_base
from sqlalchemy.sql import text

@app.route('/get_manufacturer')
def get_manufacturer():
    form = ManufacturerForm()
    form.manufacturer.choices = [
        (manufacturer.manufacturer, manufacturer.manufacturer)
        for manufacturer in Car_base.query.distinct
        (Car_base.manufacturer)
    ]
    form.manufacturer.choices.insert(0, (None, ""))
    return render_template('get_manufacturer.html', title="заполнение поля производителя автомобиля", form=form)


@app.route('/process_get_manufacturer', methods=["POST"])
def process_get_manufacturer():
    form = ManufacturerForm()
    form.manufacturer.choices = [
        (manufacturer.manufacturer, manufacturer.manufacturer)
        for manufacturer in Car_base.query.distinct
        (Car_base.manufacturer)
    ]
    if form.validate_on_submit():
        manufacturer = form.manufacturer.data
        title = "Добавление авто в гараж"
        сarinput_form = CarinputForm()
        сarinput_form.manufacturer.default = manufacturer
        сarinput_form.model.choices = [
            (model.model, model.model)
            for model in Car_base.query.filter_by(manufacturer = сarinput_form.manufacturer.data).all()
        ] 
        return render_template('carinput.html', page_title=title, form=сarinput_form)
    


@app.route('/process_carinput', methods = ['POST'])
def process_сarinput():
    title = "Добавление авто в гараж"
    сarinput_form = CarinputForm()
    сarinput_form.model.choices = [
        (model.model, model.model)
        for model in Car_base.query.filter_by(manufacturer = сarinput_form.manufacturer.data).all()
    ]
    if сarinput_form.validate_on_submit():
        car =  Vehicle(
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
