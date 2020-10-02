from flask import Blueprint, render_template, request, redirect, url_for, flash
from web_school import db
from web_school.lessons.forms import AddLessonForm
from web_school.lessons.models import Lesson
from web_school.classes.models import Studentgroup
from web_school.teachers.models import Teacher
from web_school.subject.models import Subject
from datetime import datetime, time, timedelta


lessons = Blueprint('lessons', __name__)

lesson_times = [
    time(hour=8, minute=0),
    time(hour=9, minute=0),
    time(hour=10, minute=0),
    time(hour=11, minute=0),
    time(hour=12, minute=0),
]


@lessons.route('/lessons/', methods=['GET', 'POST'])
def show_all_lessons():

    form = AddLessonForm()
    lessons = Lesson.query.all()
    group_choice = Studentgroup.query.all()
    teacher_choice = Teacher.query.all()
    subject_choice = Subject.query.all()

    if request.args.get('class'):
        name = request.args.get('class')
        kls = db.session.query(Studentgroup).filter(Studentgroup.name == name).all()
        if kls:
            return redirect(url_for('groups.kls_profile', id=kls[0].id))

    if request.args.get('name'):
        first, last = request.args.get('name').split(' ')
        teach = db.session.query(Teacher).filter(db.and_(Teacher.first_name == first, Teacher.last_name == last)).first()
        if teach:
            return redirect(url_for('teachers.teacher_profile', id=teach.id))

    form.kls.choices = group_choice
    form.teacher.choices = teacher_choice
    form.subject.choices = subject_choice
    form.start_time.choices = [i for i in lesson_times]

    if request.method == 'POST':
        if form.validate_on_submit():
            kls = form.kls.data
            teacher = form.teacher.data
            subject = form.subject.data
            day = datetime.strptime(request.form['day'], '%Y-%m-%d')
            start_time = datetime.strptime(form.start_time.data, '%H:%M:%S')
            finish_time = start_time + timedelta(minutes=45)
            lesson_in_db = Lesson.query.filter_by(kls=kls).all()
            teacher_in_db = Teacher.query.filter_by(last_name=teacher.split(' ')[-1]).first()
            teacher_lessons = Lesson.query.filter_by(teacher=teacher).all()

            if lesson_in_db:
                for les in lesson_in_db:
                    if les.day == day and les.start_time == start_time.time():
                        flash('This class already has a lesson on this day/at this time', 'warning')
                        return redirect(url_for('lessons.show_all_lessons'))

            if teacher_in_db:
                for les in teacher_lessons:
                    if les.day == day and les.start_time == start_time.time():
                        flash('This teacher already has a lesson on this day/at this time', 'warning')
                        return redirect(url_for('lessons.show_all_lessons'))

            if not teacher_in_db.subj == subject:
                flash("This teacher doesn't provide this subject", 'warning')
                return redirect(url_for('lessons.show_all_lessons'))

            new_lesson = Lesson(kls=kls, teacher=teacher, subject=subject, day=day,
                                start_time=start_time.time(), finish_time=finish_time.time())
            db.session.add(new_lesson)
            db.session.commit()
            return redirect(url_for('lessons.show_all_lessons'))

    return render_template('lessons.html', form=form, lessons=lessons)


@lessons.route('/lessons/remove/', methods=['GET', 'POST'])
def remove_lesson():
    if request.method == 'POST':
        lesson_id = request.form['delete']
        lesson_to_delete = db.session.query(Lesson).filter_by(id=lesson_id).first()
        db.session.delete(lesson_to_delete)
        db.session.commit()
        flash('Урок был удален из списка', 'warning')
    return redirect(url_for('lessons.show_all_lessons'))


