from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class AddClassForm(FlaskForm):
    grade = StringField('Grade', validators=[DataRequired()])
    letter = StringField('Letter', validators=[DataRequired()])
