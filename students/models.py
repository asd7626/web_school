from flask_login import UserMixin
from web_school import db


class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    year = db.Column(db.Integer)
    img = db.Column(db.String(40), default='default.png')
    kls = db.Column(db.String(40), db.ForeignKey('studentgroup.name'))

    def __repr__(self):
        return '({}, {}, {}, {})'.format(self.id, self.first_name, self.last_name, self.year)