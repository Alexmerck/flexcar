from datetime import datetime
from enum import unique
from webapp import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True)
    email = db.Column(db.String(120), unique = True)
    phone_number = db.Column(db.Integer, unique = True)
    password = db.Column(db.String(30), unique = False)
    events = db.relationship('Event', backref='author', lazy='dynamic')
    vehicles = db.relationship('Vehicle', backref='Name', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)
        
class Event(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(140), unique = True)
    published = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    charges = db.Column(db.Integer)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))

    def __repr__(self):
        return '<Event %r>'.format(self.title)

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
    events = db.relationship('Event', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<Vehicle %r>'.format(self.title)
