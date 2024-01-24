from task1_models import db


class StudentTask3(db.Model):
    id_stud_task3 = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    group = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    results = db.relationship('StudentResults', backref='student_task3', lazy=True)

    def __repr__(self):
        return f'Студент {self.surname} {self.name} ({self.email})'


class StudentResults(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_student_task3 = db.Column(db.Integer, db.ForeignKey('student_task3.id_stud_task3'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    result = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'{self.subject} - {self.result}'
