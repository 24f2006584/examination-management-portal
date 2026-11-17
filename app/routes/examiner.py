from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import db, ExaminerProfile, ExaminationSlot
from datetime import datetime
from app.models import Examination

examiner_bp = Blueprint('examiner', __name__, url_prefix='/examiner')

@examiner_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'examiner':
        return redirect(url_for('auth.login'))
    
    profile = ExaminerProfile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        return redirect(url_for('examiner.setup_profile'))

    if profile.status == 'Pending':
        return "Your profile is pending admin approval. Please check back later."

    slots = ExaminationSlot.query.filter_by(examiner_id=profile.id).all()
    return render_template('examiner_dashboard.html', profile=profile, slots=slots)

@examiner_bp.route('/setup_profile', methods=['GET', 'POST'])
@login_required
def setup_profile():
    if current_user.role != 'examiner':
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        name = request.form.get('name')
        department = request.form.get('department')

        new_profile = ExaminerProfile(
            user_id=current_user.id,
            name=name,
            department=department,
            status='Pending'
        )
        db.session.add(new_profile)
        db.session.commit()
        
        flash('Profile saved! Waiting for Admin approval.')
        return redirect(url_for('examiner.dashboard'))

    return render_template('examiner_setup.html')

@examiner_bp.route('/create_slot', methods=['GET', 'POST'])
@login_required
def create_slot():
    profile = ExaminerProfile.query.filter_by(user_id=current_user.id).first()
    if not profile or profile.status != 'Approved':
        flash('You must be an approved examiner to create slots.')
        return redirect(url_for('examiner.dashboard'))

    examinations = Examination.query.all()

    if request.method == 'POST':
        new_slot = ExaminationSlot(
            exam_id=request.form.get('exam_id'),
            examiner_id=profile.id,
            date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date(),
            start_time=datetime.strptime(request.form.get('start_time'), '%H:%M').time(),
            end_time=datetime.strptime(request.form.get('end_time'), '%H:%M').time(),
            capacity=int(request.form.get('capacity'))
        )
        db.session.add(new_slot)
        db.session.commit()
        flash('Examination Slot created successfully!')
        return redirect(url_for('examiner.dashboard'))

    return render_template('create_slot.html', examinations=examinations)