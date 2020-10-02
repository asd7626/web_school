from web_school import db
from flask_login import UserMixin


class Subject(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    teacher = db.relationship('Teacher', backref='subject')

    def __repr__(self):
        return self.name
    