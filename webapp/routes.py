from flask import render_template, flash, redirect, url_for, request
from flask_login.utils import login_required
from webapp import app, db
from webapp.forms import LoginForm, Signup, VehicleForm
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
from webapp.models import Vehicle, ImageSet
from webapp.forms import ManufacturerForm, Car_base, VehicleForm

import imghdr, secrets
import os
from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory
#from werkzeug.utils import secure_filename


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
@login_required
def usercar():
    user_id = current_user.id
    carlist =  Vehicle.query.filter_by(user_id=user_id).all()
    return render_template('usercars.html', title='GARAGE', user=current_user, carlist=carlist)


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
        # return render_template(
        #     'carinput.html', page_title=title, form=сarinput_form
        # )
        return render_template('image_upload.html', form = сarinput_form)


@app.route('/carinput')
@login_required
def сarinput(): 
    return render_template('carinput.html')

@app.route('/process_carinput', methods=['POST'])
@login_required
def process_сarinput(form):  
    сarinput_form = form
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
            body=сarinput_form.body.data
        )
        db.session.add(car)
        db.session.commit()
        return redirect(url_for('usercars.html'))


def validate_image(stream):
    header = stream.read(512)
    stream.seek(0) 
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

@app.route('/image_upload')
def image_upload():
    return render_template('image_upload.html')

@app.route('/image_upload', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    
    print(uploaded_file)
    print(uploaded_file.filename)
    file_name = uploaded_file.filename
    file_ext = os.path.splitext(file_name)[1].lower()
    image_name = f"{secrets.token_hex(8)}{file_ext}"
    print(image_name)
    if file_ext not in Config.UPLOAD_EXTENSIONS or \
        file_ext != validate_image(uploaded_file.stream):
        abort(400)
    uploaded_file.save(os.path.join(Config.UPLOAD_PATH, image_name))
    
    saved_picture_rout = f"{Config.UPLOAD_PATH}\{image_name}"
    print(saved_picture_rout)
    new_image = Vehicle(
        vehicle_avatar = saved_picture_rout
        )
    print(new_image)
    # db.session.add(new_image)
    # db.session.commit()
    return redirect(url_for('сarinput.html'))


@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(Config.UPLOAD_PATH, filename)