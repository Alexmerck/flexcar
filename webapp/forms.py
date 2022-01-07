from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField, SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from webapp.models import User 

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя',validators=[DataRequired()])
    password = PasswordField('Пароль',validators=[DataRequired()])
    submit = SubmitField('Продолжить',render_kw={"class":"btn btn-primary"})
    remember_me = BooleanField('Запомнить меня', default=True, render_kw ={"class": "form-check-input"})

class Signup(FlaskForm):
    username = StringField('Введите имя пользователя', validators=[DataRequired()])
    email = StringField('Ввети Email', validators=[DataRequired(), Email()])
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

class CarinputForm(FlaskForm):
    """сюда надо захерачить подгрузку картинки"""
    title = StringField('Введите имя авто (максимум 140 символов)', validators=[DataRequired()], render_kw={"class":"form-control"})
    manufacturer = StringField('Введите произовдителя авто (максимум 100 символов)', validators=[DataRequired()], render_kw={"class":"form-control"})
    model = StringField('Введите модель авто (максимум 100 символов)', validators=[DataRequired()], render_kw={"class":"form-control"})
    production_year = IntegerField('Введите год выпуска авто', validators=[DataRequired()], render_kw={"class":"form-control"})
    engine_type = IntegerField('Введите тип двигателя авто (бензин/дизель)', validators=[DataRequired()], render_kw={"class":"form-control"})
    volume = IntegerField('Введите объем двигателя авто (л)', validators=[DataRequired()], render_kw={"class":"form-control"})
    transmission_type = IntegerField('Введите тип трансмиссии (автомат/палка)', validators=[DataRequired()], render_kw={"class":"form-control"})
    body = IntegerField('Введите тип кузова авто (????)', validators=[DataRequired()], render_kw={"class":"form-control"})
    submit = SubmitField('Отправить', render_kw={"class":"btn btn-primary"})

