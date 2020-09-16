from flask_login import UserMixin
from web_school import db


class Studentgroup(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String, nullable=False)
    letter = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    students = db.relationship('Student', backref='klass')

    def __init__(self, grade, letter):
        self.grade = grade
        self.letter = letter
        self.name = self.grade + self.letter

    def __len__(self):
        return len(self.students)


