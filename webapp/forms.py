from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from webapp.models import User 
from wtforms.fields.choices import SelectField
#from webapp import db
from webapp.models import Car_base


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя',validators=[DataRequired()])
    password = PasswordField('Пароль',validators=[DataRequired()])
    submit = SubmitField('Продолжить',render_kw={"class":"btn btn-primary"})
    remember_me = BooleanField('Запомнить меня', default=True, render_kw ={"class": "form-check-input"})

class Signup(FlaskForm):
    username = StringField('Введите имя пользователя', validators=[DataRequired()])
    email = StringField('Введите e-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Введите пароль', validators=[DataRequired()])
    password2 = PasswordField(
        'Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться', render_kw={"class":"btn btn-primary"})

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Такой пользователь уже существует')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста, укажите другой e-mail')

class ManufacturerForm(FlaskForm):
    manufacturer = SelectField('Выберете производителя авто',
            choices = [
        	(manufacturer.manufacturer, manufacturer.manufacturer)
        	for manufacturer in Car_base.query.distinct
        	(Car_base.manufacturer)
        	],
            validators=[DataRequired()],  render_kw={"class":"form-control"})
    submit = SubmitField('Отправить', render_kw={"class":"btn btn-primary"})


class CarinputForm(FlaskForm):
    """сюда надо захерачить подгрузку картинки"""
    title = StringField('Введите имя авто (максимум 140 символов)', 
            validators=[DataRequired()], render_kw={"class":"form-control"})
    manufacturer = StringField('Производтель авто', 
            validators=[DataRequired()],  render_kw={"class":"form-control", 'readonly': True})
    model = SelectField('Введите модель авто (максимум 100 символов)',
            validators=[DataRequired()], render_kw={"class":"form-control"})
    production_year = IntegerField('Введите год выпуска авто', 
            validators=[DataRequired()], render_kw={"class":"form-control"})
    engine_type = SelectField('Выберете тип двигателя',
            choices = ['бензиновый','дизельный','электрический'],
            validators=[DataRequired()], render_kw={"class":"form-control"})
    volume = IntegerField('Введите объем двигателя авто (л)', 
            validators=[DataRequired()], render_kw={"class":"form-control"})
    transmission_type = SelectField('Выберете тип трансмиссии',
            choices = ['механическая','автомат','робот'],
            validators=[DataRequired()], render_kw={"class":"form-control"})
    body = SelectField('Выберете тип кузова авто',
            choices = ['седан','купе','хэтчбэк','родстер','универсал','кабриолет', 'внедорожник','кроссовер','пикап', 'фургон','минивэн','микроавтобус', 'тарга'],
            validators=[DataRequired()], render_kw={"class":"form-control"})
    submit = SubmitField('Отправить', render_kw={"class":"btn btn-primary"})

    def __init__(self, *args, **kwargs):
        super(CarinputForm, self).__init__(*args, **kwargs)
        self.model.choices = [(model.model, model.model)
        for model in Car_base.query.filter_by(
            manufacturer=self.manufacturer.data
            ).all()
		]


class VehicleForm(FlaskForm):
    """сюда надо захерачить подгрузку картинки"""
    title = StringField(render_kw={"class":"form-control"})
    manufacturer = StringField(render_kw={"class":"form-control", 'readonly': True})
    model = SelectField(render_kw={"class":"form-control"})
    production_year = IntegerField(render_kw={"class":"form-control"})
    engine_type = SelectField(render_kw={"class":"form-control"})
    volume = IntegerField(render_kw={"class":"form-control"})
    transmission_type = SelectField(render_kw={"class":"form-control"})
    body = SelectField(render_kw={"class":"form-control"})
    #submit = SubmitField('выбрать', render_kw={"class":"btn btn-primary"})        
