from config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


from webapp import routes, models
from webapp.models import User 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)