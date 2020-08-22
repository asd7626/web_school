from flask import Flask, url_for, redirect, request, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db'
db = SQLAlchemy(app)


class AddStudentForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    year = IntegerField('Year', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    year = db.Column(db.Integer)

    def __repr__(self):
        return '({}, {}, {}, {})'.format(self.id, self.first_name, self.last_name, self.year)


@app.route('/', methods=['GET', 'POST'])
@app.route('/students/', methods=['GET', 'POST'])
def show_all_students():
    form = AddStudentForm()
    sort_by = request.args.get('sort')
    direction = request.args.get('direction')
    if direction is None:
        direction = 'default'
    elif direction == 'default':
        direction = 'reversed'
    elif direction == 'reversed':
        direction = 'default'

    if request.method == 'GET':
        if sort_by == 'last_name':
            if direction == 'reversed':
                sorted_students = Student.query.order_by(desc(Student.last_name)).all()
            else:
                sorted_students = Student.query.order_by(Student.last_name).all()
        elif sort_by == 'year':
            if direction == 'reversed':
                sorted_students = Student.query.order_by(desc(Student.year)).all()
            else:
                sorted_students = Student.query.order_by(Student.year).all()
        else:
            sorted_students = Student.query.all()
        return render_template('students.html', students=sorted_students, direction=direction, form=form)

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


if __name__ == '__main__':
    app.run(host='localhost', port=1115, debug=True)