from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired


class AddClassForm(FlaskForm):
    grade = IntegerField('Grade', validators=[DataRequired()])
    letter = StringField('Letter', validators=[DataRequired()])
