from flask import Blueprint, render_template, redirect, url_for, request, flash
from web_school.forms import AddStudentForm, UpdateInfoForm
from web_school.models import Student
from flask_login import login_required
from . import app, db
from PIL import Image
import secrets
import os

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
@main.route('/students/', methods=['GET', 'POST'])
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
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
            else:
                picture_file = 'default.png'
            first_name = form.first_name.data
            last_name = form.last_name.data
            year = form.year.data
            new_student = Student(first_name=first_name, last_name=last_name,
                                  year=year, img=picture_file)
            db.session.add(new_student)
            db.session.commit()
            flash('Студент был добавлен в список', 'success')
        else:
            flash('Invalid input', 'danger')
        return redirect(url_for('main.show_all_students'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@main.route('/students/remove/', methods=['POST'])
def remove_student():
    if request.method == 'POST':
        student_id = request.form['delete']
        student_to_delete = db.session.query(Student).filter_by(id=student_id).first()
        db.session.delete(student_to_delete)
        db.session.commit()
        flash('Студент был удален из списка', 'warning')
    return redirect(url_for('main.show_all_students'))


@main.route('/students/<int:id>/', methods=['GET'])
def student_profile(id):
    if request.method == 'GET':
        student = Student.query.filter_by(id=id).first()
        first_name = student.first_name
        last_name = student.last_name
        year = student.year
        img = url_for('static', filename='images/' + student.img)
        return render_template('student_profile.html', id=id, first_name=first_name,
                               last_name=last_name, year=year, img=img)


@main.route('/students/<int:id>/edit/', methods=['GET', 'POST'])
@login_required
def edit_student_info(id):
    student_to_edit = Student.query.filter_by(id=id).first()

    form = UpdateInfoForm()
    form.first_name.data = student_to_edit.first_name
    form.last_name.data = student_to_edit.last_name
    form.year.data = student_to_edit.year

    if request.method == 'POST' and form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            student_to_edit.img = picture_file
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        year = request.form.get('year')
        student_to_edit.first_name = first_name
        student_to_edit.last_name = last_name
        student_to_edit.year = year
        db.session.commit()
        flash('Данные студента изменены', 'success')
        return redirect(url_for('main.student_profile', id=id))

    return render_template('edit_student_form.html', id=id, form=form)
