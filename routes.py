from flask import render_template, redirect, url_for, request, flash
from . import app, db
from web_school.forms import AddStudentForm, RegisterForm
from web_school.models import Student


@app.route('/', methods=['GET', 'POST'])
@app.route('/students/', methods=['GET', 'POST'])
def show_all_students():
    form = AddStudentForm()
    sort_by = request.args.get('sort')

    if request.method == 'GET':
        if sort_by == 'last_name':
            sorted_students = Student.query.order_by(Student.last_name).all()
        elif sort_by == 'year':
            sorted_students = Student.query.order_by(Student.year).all()
        else:
            sorted_students = Student.query.all()
        return render_template('students.html', students=sorted_students, form=form)

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


@app.route('/students/<int:id>/', methods=['GET', 'POST'])
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