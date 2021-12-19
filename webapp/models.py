from webapp import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    Phone_number = db.Column(db.String(11), unique=True)
    Password = db.Column(db.String(30), unique=False)

    def __repr__(self):
        return '<User %r>' % self.username
