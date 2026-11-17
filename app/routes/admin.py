from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from app.models import db, User, Course, Examination, ExaminerProfile, StudentProfile, Booking
from datetime import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'admin':
            flash('Unauthorized access.')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_courses = Course.query.count()
    total_examinations = Examination.query.count()
    total_examiners = ExaminerProfile.query.count()
    total_students = StudentProfile.query.count()
    total_bookings = Booking.query.count()

    pending_examiners = ExaminerProfile.query.filter_by(status='Pending').all()

    return render_template('admin_dashboard.html', 
                           t_courses=total_courses,
                           t_exams=total_examinations,
                           t_examiners=total_examiners,
                           t_students=total_students,
                           t_bookings=total_bookings,
                           pending_examiners=pending_examiners)

@admin_bp.route('/handle_examiner/<int:examiner_id>', methods=['POST'])
@login_required
@admin_required
def handle_examiner(examiner_id):
    examiner = ExaminerProfile.query.get_or_404(examiner_id)
    action = request.form.get('action')
    
    if action == 'approve':
        examiner.status = 'Approved'
        flash(f'Examiner {examiner.name} has been Approved!')
    elif action == 'reject':
        examiner.status = 'Rejected'
        flash(f'Examiner {examiner.name} has been Rejected.')
        
    db.session.commit()
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/create_course', methods=['GET', 'POST'])
@login_required
@admin_required
def create_course():
    if request.method == 'POST':
        course_code = request.form.get('course_code')
        course_name = request.form.get('course_name')
        
        new_course = Course(course_code=course_code, course_name=course_name)
        db.session.add(new_course)
        db.session.commit()
        flash(f'Course {course_code} created successfully!')
        return redirect(url_for('admin.dashboard'))
        
    return render_template('create_course.html')

@admin_bp.route('/create_examination', methods=['GET', 'POST'])
@login_required
@admin_required
def create_examination():
    courses = Course.query.all()
    if request.method == 'POST':
        new_exam = Examination(
            course_id=request.form.get('course_id'),
            name=request.form.get('name'),
            exam_type=request.form.get('exam_type'),
            slot_creation_start=datetime.strptime(request.form.get('slot_start'), '%Y-%m-%d').date(),
            slot_creation_end=datetime.strptime(request.form.get('slot_end'), '%Y-%m-%d').date(),
            booking_start=datetime.strptime(request.form.get('booking_start'), '%Y-%m-%d').date(),
            booking_end=datetime.strptime(request.form.get('booking_end'), '%Y-%m-%d').date()
        )
        db.session.add(new_exam)
        db.session.commit()
        flash('Examination created successfully!')
        return redirect(url_for('admin.dashboard'))
        
    return render_template('create_exam.html', courses=courses)