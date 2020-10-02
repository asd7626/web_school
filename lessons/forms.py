from flask_wtf import FlaskForm
from wtforms import SelectField, DateTimeField
from wtforms.validators import DataRequired


class AddLessonForm(FlaskForm):
    kls = SelectField('Class', validators=[DataRequired()])
    teacher = SelectField('Teacher', validators=[DataRequired()])
    subject = SelectField('Subject', validators=[DataRequired()])
    start_time = SelectField('Start Time', validators=[DataRequired()])