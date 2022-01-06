from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired
from webapp import db
from webapp.models import Car_base


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя',validators=[DataRequired()],
          render_kw={"class": "form-control"})
    password = PasswordField('Пароль',validators=[DataRequired()],
          render_kw={"class": "form-control"})
    submit = SubmitField('Продолжить',render_kw={"class":"btn btn-primary"})
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class ManufacturerForm(FlaskForm):
    manufacturer = SelectField('Выберете производителя авто', 
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
