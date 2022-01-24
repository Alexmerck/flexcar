from datetime import datetime
from enum import unique
from webapp import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True)
    email = db.Column(db.String(120), unique = True)
    phone_number = db.Column(db.Integer, unique = True)
    password = db.Column(db.String(130), unique = False)
    events = db.relationship('Event', backref='author', lazy='dynamic')
    vehicles = db.relationship('Vehicle', backref='Name', lazy='dynamic')
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)


    def __repr__(self):
        return '<User {}>'.format(self.username)
        
class Event(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(140))
    published = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    charges = db.Column(db.Integer)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    milege = db.Column(db.Integer)
    description = db.Column(db.Text)

    def __repr__(self):
        return '<Event %r>'.format(self.title)

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    manufacturer = db.Column(db.String(100))
    model = db.Column(db.String(100))
    production_year = db.Column(db.Integer)
    engine_type = db.Column(db.String(100))
    volume = db.Column(db.Integer)
    transmission_type = db.Column(db.String(100))
    body = db.Column(db.String(100))
    events = db.relationship('Event', backref='name', lazy='dynamic')
    vehicle_avatar = db.Column(db.String(120))

    def __repr__(self):
        return '<Vehicle %r>'.format(self.title)


class Car_base(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    manufacturer = db.Column(db.String(100))
    model =  db.Column(db.String(100))

    def __repr__(self):
        return '<Car_base %r>'.format(self.manufacturer)


class ImageSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(120), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))

    def __repr__(self):
        return '<ImageSet %r>'.format(self.image)