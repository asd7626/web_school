from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta


app = Flask(__name__)
app.config['SECRET_KEY'] = 'asd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(hours=1)
app.config['IMAGE_UPLOADS'] = "C:/Users/Admin/PycharmProjects/Flask/web_school/static/images"
app.config['ALLOWED_IMAGE_EXTENSIONS'] = ['PNG', 'JPEG', 'JPG', 'GIF']

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from .main import main as main_blueprint
app.register_blueprint(main_blueprint)


from web_school.models import User, Student
from web_school import routes

