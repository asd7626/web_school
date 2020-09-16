from flask import Blueprint, render_template, redirect, url_for, request, flash
from web_school.users.forms import RegisterForm, LoginForm, RequestResetForm, ResetPasswordForm
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from web_school.users.models import User
from flask_login import login_required
from web_school import db, mail
from flask_mail import Message


users = Blueprint('users', __name__)


@users.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    error = None
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            user = User.query.filter_by(email=email).first()
            if user:
                error = 'Email already exists. Try to '
            else:
                new_user = User(username=username, email=email, password=generate_password_hash(password, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                flash('You have been registered. Log in to your account.', 'success')
                return redirect(url_for('users.login'))

    return render_template('register.html', form=form, error=error)


@users.route('/login/', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            remember = True if request.form.get('remember') else False

            user = User.query.filter_by(email=email).first()
            if not user or not check_password_hash(user.password, password):
                error = 'Invalid email or password. Try again, please'
            else:
                login_user(user, remember=remember)
                next_page = request.args.get('next')
                flash('You are now logged in as "{}"'.format(user.username), 'success')
                return redirect(next_page) if next_page else redirect(url_for('students.show_all_students'))
    return render_template('login.html', form=form, error=error)


@users.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'warning')
    return redirect(url_for('students.show_all_students'))


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='Student app',
                  recipients=[user.email])
    msg.body = f"""To reset your password, visit the following link:
{url_for('auth.reset_token', token=token, _external=True)}

If you did not make this request, then simply ignore this message and no changes will be made.
"""
    mail.send(msg)


@users.route('/reset_password/', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('students.show_all_students'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Email has been sent to your email with instructions')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('students.show_all_students'))

    user = User.verify_reset_token(token)
    if user is None:
        flash('This is an invalid of expired token', 'warning')
        return redirect(url_for('users.reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated. You are now able to log in')
        return redirect(url_for('users.login'))

    return render_template('reset_token.html', form=form, title='Reset Password')