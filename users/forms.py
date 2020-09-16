from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators, ValidationError
from web_school.users.models import User


class RegisterForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=2, max=20)])
    email = StringField('Email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=2, max=40)])
    confirm_password = PasswordField('Confirm Password', [validators.DataRequired(), validators.EqualTo('password')])


class LoginForm(FlaskForm):
    email = StringField('Email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired()])


class RequestResetForm(FlaskForm):
    email = StringField('Email', [validators.DataRequired(), validators.Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with such an email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=2, max=40)])
    confirm_password = PasswordField('Confirm Password', [validators.DataRequired(), validators.EqualTo('password')])
    submit = SubmitField('Reset Password')