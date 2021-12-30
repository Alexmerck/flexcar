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


class Event(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(140), unique = True)
    published = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    charges = db.Column(db.Integer)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(140), unique = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    manufacturer = db.Column(db.String(100))
    model = db.Column(db.String(100))
    production_year = db.Column(db.Integer)
    engine_type = db.Column (db.Integer)
    volume = db.Column(db.Integer)
    transmission_type = db.Column(db.Integer)
    body = db.Column(db.Integer)
    events = db.relationship('Event', backref='name', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.username
