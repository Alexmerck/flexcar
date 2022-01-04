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

class CarinputForm(FlaskForm):
    """сюда надо захерачить подгрузку картинки"""
    title = StringField('Введите имя авто (максимум 140 символов)', 
            validators=[DataRequired()], render_kw={"class":"form-control"})
    manufacturer = SelectField('Введите произовдителя авто (максимум 100 символов)', 
            validators=[DataRequired()],  render_kw={"class":"form-control"})
    def __init__(self, *args, **kwargs):
        super(CarinputForm, self).__init__(*args, **kwargs)
        self.manufacturer.choices = [
                                    (manufacturer.id, manufacturer.manufacturer) 
                                    for manufacturer in Car_base.query.distinct
                                    (Car_base.manufacturer)
                                    ]
        #print(self.manufacturer.choices)
    model = SelectField('Введите модель авто (максимум 100 символов)',
            validators=[DataRequired()], render_kw={"class":"form-control"})


    production_year = IntegerField('Введите год выпуска авто', 
            validators=[DataRequired()], render_kw={"class":"form-control"})
    engine_type = IntegerField('Введите тип двигателя авто (бензин/дизель)', 
            validators=[DataRequired()], render_kw={"class":"form-control"})
    volume = IntegerField('Введите объем двигателя авто (л)', 
            validators=[DataRequired()], render_kw={"class":"form-control"})
    transmission_type = IntegerField('Введите тип трансмиссии (автомат/палка)', 
            validators=[DataRequired()], render_kw={"class":"form-control"})
    body = IntegerField('Введите тип кузова авто (????)', 
            validators=[DataRequired()], render_kw={"class":"form-control"})
    submit = SubmitField('Отправить', render_kw={"class":"btn btn-primary"})
