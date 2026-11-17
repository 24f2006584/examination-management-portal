from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), nullable=False) # 'admin', 'examiner', 'student'

class StudentProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    user = db.relationship('User', backref='student_profile')

class ExaminerProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    department = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(50), default='Pending') # Admin must approve
    user = db.relationship('User', backref='examiner_profile')

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(50), unique=True, nullable=False)
    course_name = db.Column(db.String(150), nullable=False)
    examinations = db.relationship('Examination', backref='course', lazy=True)

class Examination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    exam_type = db.Column(db.String(50), nullable=False) 
    slot_creation_start = db.Column(db.Date, nullable=False)
    slot_creation_end = db.Column(db.Date, nullable=False)
    booking_start = db.Column(db.Date, nullable=False)
    booking_end = db.Column(db.Date, nullable=False)
    slots = db.relationship('ExaminationSlot', backref='examination', lazy=True)

class ExaminationSlot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('examination.id'), nullable=False)
    examiner_id = db.Column(db.Integer, db.ForeignKey('examiner_profile.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    bookings = db.relationship('Booking', backref='slot', lazy=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profile.id'), nullable=False)
    slot_id = db.Column(db.Integer, db.ForeignKey('examination_slot.id'), nullable=False)
    status = db.Column(db.String(50), default='Booked')
    marks_awarded = db.Column(db.Float, nullable=True)
    remarks = db.Column(db.Text, nullable=True)