from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from web_school.forms import RegisterForm, LoginForm
from web_school.models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            user = User.query.filter_by(email=email).first()
            if user:
                flash('Email already exists', 'danger')
                return redirect(url_for('auth.register'))

            new_user = User(username=username, email=email, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('You have been registered. Log in to your account.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            remember = True if request.form.get('remember') else False

            user = User.query.filter_by(email=email).first()
            if not user or not check_password_hash(user.password, password):
                flash('Invalid email or password. Try again, please', 'danger')
                return redirect(url_for('auth.login'))
            login_user(user, remember=remember)
            return redirect(url_for('main.show_all_students'))
    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.show_all_students'))