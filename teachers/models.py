from web_school import db
from flask_login import UserMixin


class Teacher(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    subj = db.Column(db.String(50), db.ForeignKey('subject.name'))
    lessons = db.relationship('Lesson', backref='teach')

    def __repr__(self):
        return self.first_name + ' ' + self.last_name


