from web_school import db
from flask import Blueprint, render_template, redirect, url_for, request, flash
from web_school.teachers.forms import AddTeacherForm
from web_school.teachers.models import Teacher
from web_school.subject.models import Subject
from web_school.lessons.models import Lesson


teachers = Blueprint('teachers', __name__)


@teachers.route('/teachers/', methods=['GET', 'POST'])
def show_all_teachers():
    form = AddTeacherForm()
    choices = [subj.name for subj in Subject.query.all()]
    form.subject.choices = choices
    teachers = Teacher.query.all()
    if request.method == 'POST':
        if form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            subj = form.subject.data
            new_teacher = Teacher(first_name=first_name, last_name=last_name, subj=subj)
            db.session.add(new_teacher)
            db.session.commit()
            flash('New Teacher was successfully added', 'success')
        else:
            flash('Invalid Input', 'danger')
        return redirect(url_for('teachers.show_all_teachers'))
    return render_template('teachers.html', teachers=teachers, form=form)


@teachers.route('/teachers/<int:id>', methods=['GET', 'POST'])
def teacher_profile(id):
    teacher = Teacher.query.filter_by(id=id).first()
    first_name = teacher.first_name
    last_name = teacher.last_name
    subj = teacher.subj

    return render_template('teacher_profile.html', first_name=first_name, last_name=last_name, subj=subj)


@teachers.route('/teachers/remove/', methods=['GET', 'POST'])
def remove_teacher():
    if request.method == 'POST':
        teacher_id = request.form['delete']
        teacher_to_delete = db.session.query(Teacher).filter_by(id=teacher_id).first()
        lessons_to_delete = db.session.query(Lesson).filter_by(teacher=teacher_to_delete.first_name + ' ' + teacher_to_delete.last_name).all()
        for lesson in lessons_to_delete:
            db.session.delete(lesson)
        db.session.delete(teacher_to_delete)
        db.session.commit()
        flash('Учитель и его уроки были удалены из списка', 'warning')
    return redirect(url_for('teachers.show_all_teachers'))

