from flask_wtf import FlaskForm
from wtforms import Form, StringField, IntegerField,  PasswordField, validators
from wtforms.validators import DataRequired, Length


class AddStudentForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    year = IntegerField('Year', validators=[DataRequired()])


class RegisterForm(Form):
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=2, max=20)])
    email = StringField('Email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=6, max=40)])
    confirm_password = PasswordField('Confirm Password', [validators.DataRequired(), validators.EqualTo('password')])