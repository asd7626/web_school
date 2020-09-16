from flask import Blueprint, render_template, redirect, url_for, request, flash
from web_school.classes.forms import AddClassForm
from web_school.students.models import Student
from web_school.classes.models import Studentgroup
from sqlalchemy import and_
from web_school import db


groups = Blueprint('groups', __name__)


@groups.route('/classes/', methods=['GET', 'POST'])
def show_all_classes():
    form = AddClassForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            grade = form.grade.data
            letter = form.letter.data
            name = grade + letter
            group = db.session.query(Studentgroup).filter_by(name=name).scalar() is not None
            if group:
                flash('This class already exists', 'danger')
                return redirect(url_for('groups.show_all_classes'))
            new_kls = Studentgroup(grade=grade, letter=letter)
            db.session.add(new_kls)
            db.session.commit()
            flash('New Class was successfully created!', 'success')
            return redirect(url_for('groups.show_all_classes'))
    classes = Studentgroup.query.all()
    students = Student.query.filter_by(kls=Studentgroup.name).all()
    return render_template('classes.html', classes=classes, students=students, form=form)


@groups.route('/classes/<int:id>', methods=['GET', 'POST'])
def kls_profile(id):
    group = Studentgroup.query.filter_by(id=id).first()
    students = group.students
    name = group.name
    return render_template('class_profile.html', students=students, name=name)


@groups.route('/classes/remove/', methods=['POST'])
def remove_kls():
    if request.method == 'POST':
        kls_id = request.form['delete']
        kls_to_delete = db.session.query(Studentgroup).filter_by(id=kls_id).first()
        students = kls_to_delete.students
        for student in students:
            db.session.delete(student)
        db.session.delete(kls_to_delete)
        db.session.commit()
        flash('Класс был удален из списка', 'warning')
    return redirect(url_for('groups.show_all_classes'))