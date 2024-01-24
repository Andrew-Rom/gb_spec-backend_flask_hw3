import os
import random

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash

from task1_models import db, Student, Faculty
from task2_models import Book, Author
from task3_models import StudentTask3, StudentResults
from task4_forms import RegisterForm
from task4_models import User
from task5_forms import Register
from task6_forms import Register_form6
from task7_forms import Register_form7
from task8_forms import Register_form8
from task8_models import User8

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SECRET_KEY'] = b'2f5db05144a1008ad353eac6ffa199cb5112c9828735d4974ef930d091a94f0b'
csrf = CSRFProtect(app)
db.init_app(app)

FIRST_NAMES = ['John', 'Bob', 'Kate', 'Ann', 'Patric', 'Sid', 'Iren',
               'Henry', 'Elona', 'Linda', 'Nick', 'Rick', 'Tom', 'Jane']
LAST_NAMES = ['Doe', 'Black', 'White', 'Mask', 'Bess', 'Lee', 'Russo', 'Prost', 'Senna', 'Miles']
SPEC_NAMES = ['Motorsport', 'Math', 'Computer vision', 'Python', 'Constructing', 'Chemistry']


@app.route('/')
@app.route('/index/')
@app.route('/index.html/')
def index():
    if os.path.exists('instance/mydatabase.db'):
        db.drop_all()
    db.create_all()
    context = {'page_name': 'Главная'}
    return render_template('index.html', **context)


@app.route('/task1/')
@app.route('/task1.html/')
def task1():
    for _ in range(9):
        student = Student(name=random.choice(FIRST_NAMES),
                          surname=random.choice(LAST_NAMES),
                          age=random.randint(18, 30),
                          gender=random.choice(['мужской', 'женский']),
                          group=random.choice([201, 202, 301, 550]),
                          id_faculty=random.choice([1, 2, 3, 4]))
        db.session.add(student)
        db.session.commit()

    for i in range(5):
        faculty = Faculty(name=SPEC_NAMES[i])
        db.session.add(faculty)
        db.session.commit()

    students = Student.query.all()
    context = {'students': students}

    return render_template('task1.html', **context)


@app.route('/task2/')
@app.route('/task2.html/')
def task2():
    for _ in range(20):
        book = Book(title=random.choice(SPEC_NAMES),
                    published=random.randint(1950, 2024),
                    copies=random.randint(1, 1_000_000),
                    id_author=random.choice([1, 2, 3, 4]))
        db.session.add(book)
        db.session.commit()

    for _ in range(5):
        author = Author(name=random.choice(FIRST_NAMES),
                        surname=random.choice(LAST_NAMES))
        db.session.add(author)
        db.session.commit()

    books = Book.query.all()
    context = {'books': books}

    return render_template('task2.html', **context)


@app.route('/task3/')
@app.route('/task3.html/')
def task3():
    for _ in range(5):
        student_name = random.choice(FIRST_NAMES)
        student_surname = random.choice(LAST_NAMES)
        student_email = f'{student_name[0].lower()}_{student_surname.lower()}@' \
                        + random.choice(['mail', 'gmail', 'yandex', 'yahoo']) \
                        + random.choice(['.com', '.ru', '.net', '.vn'])
        student_task3 = StudentTask3(name=student_name,
                                     surname=student_surname,
                                     group=random.choice([201, 202, 301, 550]),
                                     email=student_email)
        db.session.add(student_task3)
        db.session.commit()

    for i in range(25):
        result = StudentResults(subject=SPEC_NAMES[random.randint(0, len(SPEC_NAMES) - 1)],
                                result=random.choice([5, 4, 3, 2]),
                                id_student_task3=random.randint(1, 5))
        db.session.add(result)
        db.session.commit()

    students_task3 = StudentTask3.query.all()
    context = {'students_task3': students_task3}

    return render_template('task3.html', **context)


@app.route('/task4/', methods=['GET', 'POST'])
@app.route('/task4.html/', methods=['GET', 'POST'])
def task4():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        new_user = User(name=form.name.data,
                        email=form.email.data,
                        password=form.password.data)
        user = User.query.filter(User.name == new_user.name, User.email == new_user.email).first()
        if user:
            msg = 'Пользователь с такими данными уже зарегистрирован'
        else:
            msg = 'Пользователь успешно зарегистрирован'
            db.session.add(new_user)
            db.session.commit()
        context = {'msg': msg}
        return render_template('task4.html', **context, form=form)
    return render_template('task4.html', form=form)


@app.route('/task5/', methods=['GET', 'POST'])
@app.route('/task5.html/', methods=['GET', 'POST'])
def task5():
    form = Register()
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        birthday = form.birthday.data
        context = {'name': name, 'email': email, 'birthday': birthday}
        return render_template('task5_confirm.html', **context)
    return render_template('task5.html', form=form)


@app.route('/task6/', methods=['GET', 'POST'])
@app.route('/task6.html/', methods=['GET', 'POST'])
def task6():
    form = Register_form6()
    if request.method == 'POST' and form.validate():
        flash(f'Пользователь {form.name.data} - {form.email.data} успешно зарегистрирован')
        return redirect('/task6')
    return render_template('task6.html', form=form)


@app.route('/task7/', methods=['GET', 'POST'])
@app.route('/task7.html/', methods=['GET', 'POST'])
def task7():
    form = Register_form7()
    if request.method == 'POST' and form.validate():
        flash(f'Пользователь {form.name.data} {form.surname.data} - {form.email.data} успешно зарегистрирован')
        return redirect('/task7')
    return render_template('task7.html', form=form)


@app.route('/task8/', methods=['GET', 'POST'])
@app.route('/task8.html/', methods=['GET', 'POST'])
def task8():
    form = Register_form8()
    if request.method == 'POST' and form.validate():
        hash = generate_password_hash(form.password.data)
        new_user = User8(name=form.name.data,
                         surname=form.surname.data,
                         email=form.email.data,
                         password=hash)
        user = User8.query.filter(User8.name == new_user.name,
                                  User8.surname == new_user.surname,
                                  User8.email == new_user.email).first()
        if user:
            flash('Пользователь с такими данными уже зарегистрирован')
            return redirect(url_for('task8'))
        else:
            db.session.add(new_user)
            db.session.commit()
            flash(f'Пользователь {form.name.data} {form.surname.data} - {form.email.data} успешно зарегистрирован')
            return redirect(url_for('task8'))
    return render_template('task8.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
