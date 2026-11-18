from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import db, StudentProfile, Booking, ExaminationSlot

student_bp = Blueprint('student', __name__, url_prefix='/student')

@student_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'student':
        return redirect(url_for('auth.login'))
    
    profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        return redirect(url_for('student.setup_profile'))

    available_slots = ExaminationSlot.query.all()
    bookings = Booking.query.filter_by(student_id=profile.id).all()
    booked_slot_ids = [b.slot_id for b in bookings]

    return render_template('student_dashboard.html', 
                           profile=profile, 
                           available_slots=available_slots, 
                           bookings=bookings, 
                           booked_slot_ids=booked_slot_ids)

@student_bp.route('/setup_profile', methods=['GET', 'POST'])
@login_required
def setup_profile():
    if current_user.role != 'student':
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        name = request.form.get('name')
        new_profile = StudentProfile(user_id=current_user.id, name=name)
        db.session.add(new_profile)
        db.session.commit()
        
        flash('Profile saved successfully!')
        return redirect(url_for('student.dashboard'))

    return render_template('student_setup.html')

@student_bp.route('/book/<int:slot_id>', methods=['POST'])
@login_required
def book(slot_id):
    profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
    slot = ExaminationSlot.query.get_or_404(slot_id)

    current_bookings = Booking.query.filter_by(slot_id=slot_id).count()
    if current_bookings >= slot.capacity:
        flash('This slot is full.')
        return redirect(url_for('student.dashboard'))

    existing_booking = Booking.query.filter_by(student_id=profile.id, slot_id=slot_id).first()
    if existing_booking:
        flash('You have already booked this slot.')
        return redirect(url_for('student.dashboard'))

    new_booking = Booking(student_id=profile.id, slot_id=slot_id)
    db.session.add(new_booking)
    db.session.commit()
    
    flash('Successfully booked the examination slot!')
    return redirect(url_for('student.dashboard'))