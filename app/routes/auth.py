from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from app.models import User
from werkzeug.security import generate_password_hash 
from app.models import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard')) 
            elif user.role == 'student':
                return redirect(url_for('student.dashboard'))
            elif user.role == 'examiner':
                return redirect(url_for('examiner.dashboard')) 
        else:
            flash('Invalid username or password')
            
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        role = request.form.get('role')
        username = request.form.get('username')
        password = request.form.get('password')

        if role == 'admin':
            flash('Admin registration is not allowed.')
            return redirect(url_for('auth.register'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password_hash=hashed_password, role=role)
        
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in to complete your profile.')
        return redirect(url_for('auth.login'))

    return render_template('register.html')