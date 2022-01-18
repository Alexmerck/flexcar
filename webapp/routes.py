from flask import render_template, flash, redirect, url_for, request
from flask_login.utils import login_required
from webapp import app, db
from webapp.forms import LoginForm, Signup, CarinputForm, ManufacturerForm, Car_base
from flask_login import LoginManager, login_user, logout_user, current_user
from webapp.models import User, Vehicle
from getpass import getpass
from sqlalchemy.orm import selectinload
from config import Config
from webapp.models import User 
from webapp.forms import CarinputForm
from webapp import db
from webapp.models import Vehicle, ImageSet, Event
from webapp.forms import ManufacturerForm, Car_base, VehicleForm

import imghdr, secrets
import os
from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory
from webapp.scripts.save_image import upload_files



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
    return redirect(url_for('index'))

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


@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(Config.UPLOAD_PATH, filename)


@app.route('/current_car/<car_id>')
def current_car(car_id):
    cid = car_id
    title = 'Карточка автомобиля'
    car =  Vehicle.query.filter_by(id=cid).first()
    events = Event.query.filter_by(vehicle_id=cid).all()
    return render_template('current_car.html', title=title, car=car, events=events)    