from flask import Flask, url_for, redirect, request, render_template, flash
from flask_sqlalchemy import SQLAlchemy
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
def show_all_students():
    form = AddStudentForm()
    students_db = Student.query.all()
    amount = len(students_db)
    return render_template('students.html', students=students_db, form=form, amount=amount)


@app.route('/add/', methods=['POST'])
def add_student():
    form = AddStudentForm()
    if form.validate_on_submit():
        new_student = Student(first_name=form.first_name.data, last_name=form.last_name.data, year=form.year.data)
        db.session.add(new_student)
        db.session.commit()
        flash('Студент был добавлен в список', 'success')
    else:
        flash('Invalid input', 'danger')
    return redirect(url_for('show_all_students'))


@app.route('/remove/', methods=['DELETE', 'POST'])
def remove_student():
    student_id = request.form['delete']
    student_to_delete = db.session.query(Student).filter_by(id=student_id).first()
    db.session.delete(student_to_delete)
    db.session.commit()
    flash('Студент был удален из списка', 'warning')
    return redirect(url_for('show_all_students'))


if __name__ == '__main__':
    app.run(host='localhost', port=1115, debug=True)