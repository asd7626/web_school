from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from . import app, db
from web_school.forms import AddStudentForm, RegisterForm, LoginForm
from web_school.models import Student, User
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/', methods=['GET', 'POST'])
@app.route('/students/', methods=['GET', 'POST'])
def show_all_students():
    form = AddStudentForm()
    sort_by = request.args.get('sort')
    direction = request.args.get('direction')
    
    if request.method == 'GET':
        if sort_by == 'last_name':
            students = db.engine.execute('select * from student order by last_name' + ' ' + direction)
        elif sort_by == 'year':
            students = db.engine.execute('select * from student order by year' + ' ' + direction)
        else:
            students = db.engine.execute('select * from student')
        return render_template('students.html', students=students, form=form, sort=sort_by, direction=direction)

    if request.method == 'POST':
        if form.validate_on_submit():
            new_student = Student(first_name=form.first_name.data, last_name=form.last_name.data, year=form.year.data)
            db.session.add(new_student)
            db.session.commit()
            flash('Студент был добавлен в список', 'success')
        else:
            flash('Invalid input', 'danger')
        return redirect(url_for('show_all_students'))


@app.route('/students/remove/', methods=['POST'])
def remove_student():
    if request.method == 'POST':
        student_id = request.form['delete']
        student_to_delete = db.session.query(Student).filter_by(id=student_id).first()
        db.session.delete(student_to_delete)
        db.session.commit()
        flash('Студент был удален из списка', 'warning')
    return redirect(url_for('show_all_students'))


@app.route('/students/<int:id>/', methods=['GET'])
def student_profile(id):
    if request.method == 'GET':
        student = Student.query.filter_by(id=id).first()
        first_name = student.first_name
        last_name = student.last_name
        year = student.year
        return render_template('student_profile.html', id=id, first_name=first_name, last_name=last_name, year=year)


@app.route('/students/<int:id>/edit/', methods=['GET', 'POST'])
def edit_student_info(id):
    student_to_edit = Student.query.filter_by(id=id).first()

    form = AddStudentForm()
    form.first_name.data = student_to_edit.first_name
    form.last_name.data = student_to_edit.last_name
    form.year.data = student_to_edit.year

    if request.method == 'POST'and form.validate_on_submit():
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        year = request.form.get('year')
        student_to_edit.first_name = first_name
        student_to_edit.last_name = last_name
        student_to_edit.year = year
        db.session.commit()
        flash('Данные студента изменены', 'success')
        return redirect(url_for('student_profile', id=id))

    return render_template('edit_student_form.html', id=id, form=form)


@app.route('/register/', methods=['GET', 'POST'])
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
                return redirect(url_for('register'))

            new_user = User(username=username, email=email, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('You have been registered. Log in to your account.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login/', methods=['GET', 'POST'])
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
                return redirect(url_for('login'))
            login_user(user, remember=remember)
            return redirect(url_for('show_all_students'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('show_all_students'))