from email.policy import default
from flask import render_template, flash, redirect, url_for, request
from flask_login.utils import login_required
from webapp import app, db
from webapp.forms import LoginForm, Signup, CarinputForm, ManufacturerForm, Car_base, EventForm
from flask_login import LoginManager, login_user, logout_user, current_user
from webapp.models import User, Vehicle, Event
from getpass import getpass
from sqlalchemy.orm import selectinload
from config import Config
from webapp.models import User 
from webapp.forms import CarinputForm
from webapp import db
from webapp.models import Vehicle, ImageSet, Event
from webapp.forms import ManufacturerForm, Car_base, VehicleForm
import locale
import imghdr, secrets
import os
from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory
from webapp.scripts.save_image import upload_files
from webapp.scripts.parser import parser_prices
from statistics import StatisticsError, mean

locale.setlocale(locale.LC_ALL, '')


@app.route('/')
@app.route('/index')
@login_required

def index():
    title = 'Flexcar. Easy to own'
    user = {'username': 'Alex'}
    return render_template('index.html', title=title, user=user)


@app.route('/login')
def login():
    title = 'Flexcar. Easy to own'
    login_form = LoginForm()
    return render_template('login.html', title=title, form=login_form)

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
    title = 'Flexcar. Easy to own'
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
    return render_template('signup.html', title=title, form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/usercars')
@login_required
def usercar():
    user_id = current_user.id
    carlist =  Vehicle.query.filter_by(user_id=user_id).all()
    return render_template('usercars.html', title='GARAGE', user=current_user, carlist=carlist)


@app.route('/get_manufacturer')
def get_manufacturer():
    title = 'Заполнение поля производителя автомобиля'
    form = ManufacturerForm()
    return render_template('get_manufacturer.html', title=title, form=form)


@app.route('/process_get_manufacturer', methods=["POST"])
def process_get_manufacturer():
    form = ManufacturerForm()
    if form.validate_on_submit():
        manufacturer = form.manufacturer.data
        title = "Добавление авто в гараж"
        сarinput_form = CarinputForm()
        сarinput_form.manufacturer.default = manufacturer
        return render_template(
            'carinput.html', title=title, form=сarinput_form
        )


@app.route('/process_carinput', methods=['POST'])
@login_required
def process_сarinput():  
    сarinput_form = CarinputForm()
    if сarinput_form.validate_on_submit():
        car = Vehicle(
            user_id= current_user.id,
            title=сarinput_form.title.data,
            manufacturer=сarinput_form.manufacturer.data,
            model=сarinput_form.model.data,
            production_year=сarinput_form.production_year.data,
            engine_type=сarinput_form.engine_type.data,
            volume=сarinput_form.volume.data,
            transmission_type=сarinput_form.transmission_type.data,
            body=сarinput_form.body.data,
            vehicle_avatar=upload_files()
        )
        db.session.add(car)
        db.session.commit()
        return redirect(url_for('usercar'))


@app.route ('/events')
@login_required
def events():
    form = EventForm()
    title = 'Flexcar. Easy to own'
    user_id = current_user.id
    vehicles = Vehicle.query.filter_by(user_id=user_id).all()
    events = Event.query.filter_by(user_id=user_id).all()     
    form.car_title.choices = [(i.id, i.title) for i in vehicles] 
    if not vehicles:
        flash('Чтобы добавлять события, необходимо сначала добавить автомобиль')       
    if events == None:
        flash('Вы еще не добавили ни одного события')  
    return render_template('events.html', title=title, form=form, user=current_user, events=events, vehicles=vehicles)
    
    
 

@app.route ('/process_event', methods=['POST'])
@login_required
def creating():
    form = EventForm()
    available_vehicles=db.session.query(Vehicle).filter(Vehicle.user_id == current_user.id).all()
    form.car_title.choices = [(i.id, i.title) for i in available_vehicles]
    if form.validate_on_submit():
        event = Event(
            user_id= current_user.id,
            title=form.title.data,
            charges = form.charges.data,
            vehicle_id = form.car_title.data,
            milege = form.milege.data,
            description = form.description.data,
        )
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('events'))


@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(Config.UPLOAD_PATH, filename)


@app.route('/current_car/<car_id>')
def current_car(car_id):
    title = 'Карточка автомобиля'
    car =  Vehicle.query.filter_by(id=car_id).first()
    events = Event.query.filter_by(vehicle_id=car_id).all()
    return render_template('current_car.html', title=title, car=car, events=events)    


@app.route('/change_car_data/<car_id>')
def change_car_data(car_id):
    title = 'Изменение карточки автомобиля'
    car =  Vehicle.query.filter_by(id=car_id).first()
    form = CarinputForm(
        title=car.title,
        manufacturer=car.manufacturer,
        model=car.model,
        production_year=car.production_year,
        engine_type=car.engine_type,
        volume=car.volume,
        transmission_type=car.transmission_type,
        body=car.body
        )
    return render_template('change_car_data.html', title=title, car=car, form=form)


@app.route('/change_car_data_in_progress/<car_id>', methods=["POST"])
def change_car_data_in_progress(car_id):
    car =  Vehicle.query.filter_by(id=car_id).first()
    form = CarinputForm()
    if form.validate_on_submit():
        car.title=form.title.data
        car.manufacturer=form.manufacturer.data
        car.model=form.model.data
        car.production_year=form.production_year.data
        car.engine_type=form.engine_type.data
        car.volume=form.volume.data
        car.transmission_type=form.transmission_type.data
        car.body=form.body.data
        if request.files['file']:
            car.vehicle_avatar=upload_files()
        else:
            car.vehicle_avatar=car.vehicle_avatar
        db.session.commit()
        title = 'Карточка автомобиля'
        events = Event.query.filter_by(vehicle_id=car_id).all()
        return render_template('current_car.html', title=title, car=car, events=events)

@app.route('/current_event/<event_id>')
def current_event(event_id):
    title = 'Событие'
    event = Event.query.filter_by(id=event_id).first()
    return render_template('current_event.html', title=title, event=event) 


@app.route('/price_parser/<car_id>')
@login_required
def price_parser(car_id):
    title = 'Cтоимость автомобиля на рынке б/у автомобилей'
    car =  Vehicle.query.filter_by(id=car_id).first()
    manufacturer = car.manufacturer.lower()
    model = car.model.lower()
    production_year = car.production_year
    try:
        price_list = parser_prices(manufacturer, model, production_year)
        mid_price = locale.format('%d', round(mean(price_list)), grouping=True)
        max_price = locale.format('%d', max(price_list), grouping=True)
        min_price = locale.format('%d', min(price_list), grouping=True)
        return render_template('price_parser.html', title=title, mid_price=mid_price, max_price=max_price, min_price=min_price)
    except StatisticsError:
        flash('Невозможно рассчитать стоимость автомобиля')
        return redirect(url_for('current_car', car_id=car.id))