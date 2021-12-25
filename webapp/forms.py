from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class CarinputForm(FlaskForm):
    """сюда надо захерачить подгрузку картинки"""
    title = StringField('Введите имя авто (максимум 140 символов)', validators=[DataRequired()])
    manufacturer = StringField('Введите произовдителя авто (максимум 100 символов)', validators=[DataRequired()])
    model = StringField('Введите модель авто (максимум 100 символов)', validators=[DataRequired()])
    production_year = StringField('Введите год выпуска авто', validators=[DataRequired()])
    engine_type = StringField('Введите тип двигателя авто (бензин/дизель)', validators=[DataRequired()])
    volume = StringField('Введите объем двигателя авто (л)', validators=[DataRequired()])
    transmission_type = StringField('Введите тип трансмиссии (автомат/палка)', validators=[DataRequired()])
    body = StringField('Введите тип кузова авто (????)', validators=[DataRequired()])
    submit = SubmitField('Отправить')
