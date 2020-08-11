from flask import Flask, url_for, redirect, request, render_template, flash
import sqlite3
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length


app = Flask(__name__)
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='asd'
))

students = [
    ('Alex', 'Herman', '1994'),
    ('Eugene', 'Zaika', '1994')
]


class AddStudentForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    year = IntegerField('Year', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


@app.route('/', methods=['GET', 'POST'])
def show_all_students():
    form = AddStudentForm()
    conn = sqlite3.connect('student.db')
    cur = conn.cursor()
    cur.execute('SELECT rowid, * FROM students')
    students_db = cur.fetchall()
    conn.commit()
    conn.close()
    return render_template('students.html', students=students_db, form=form)


@app.route('/add/', methods=['POST'])
def add_student():
    form = AddStudentForm()
    if form.validate_on_submit():
        conn = sqlite3.connect('student.db')
        cur = conn.cursor()
        cur.execute('INSERT INTO students VALUES (?, ?, ?)', (form.first_name.data, form.last_name.data, form.year.data))
        conn.commit()
        conn.close()
        flash('Студент был добавлен в список', 'success')
    else:
        flash('Invalid input', 'danger')
    return redirect(url_for('show_all_students'))


@app.route('/remove/', methods=['POST'])
def remove_student():
    conn = sqlite3.connect('student.db')
    cur = conn.cursor()
    student_id = request.form['id']
    cur.execute('DELETE from students WHERE rowid=(?)', (student_id, ))
    conn.commit()
    conn.close()
    flash('Студент был удален из списка', 'warning')
    return redirect(url_for('show_all_students'))


if __name__ == '__main__':
    app.run(host='localhost', port=1115, debug=True)