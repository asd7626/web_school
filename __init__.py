from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from web_school.config import Config


db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from web_school.classes.routes import groups
    from web_school.students.routes import students
    from web_school.teachers.routes import teachers
    from web_school.users.routes import users
    from web_school.errors.routes import errors

    app.register_blueprint(students)
    app.register_blueprint(groups)
    app.register_blueprint(teachers)
    app.register_blueprint(users)
    app.register_blueprint(errors)

    @app.before_first_request
    def create_tables():
        db.create_all()

    return app

