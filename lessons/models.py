from flask_login import UserMixin
from web_school import db


class Lesson(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    kls = db.Column(db.String(40), db.ForeignKey('studentgroup.name'), nullable=False)
    teacher = db.Column(db.String(40), db.ForeignKey('teacher.last_name'), nullable=False)
    subject = db.Column(db.String(40), nullable=False)
    day = db.Column(db.DateTime, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    finish_time = db.Column(db.Time, nullable=False)

    def __init__(self, kls, teacher, subject, day, start_time, finish_time):
        self.kls = kls
        self.teacher = teacher
        self.subject = subject
        self.day = day
        self.start_time = start_time
        self.finish_time = finish_time

    def __iter__(self):
        return iter(self)

