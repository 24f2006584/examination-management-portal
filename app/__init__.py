from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from .models import db, User

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'disguised'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes.auth import auth_bp
    from .routes.admin import admin_bp
    from .routes.examiner import examiner_bp
    from .routes.student import student_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(examiner_bp)
    app.register_blueprint(student_bp)

    with app.app_context():
        db.create_all()
        
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            hashed_password = generate_password_hash('admin123')
            new_admin = User(username='admin', password_hash=hashed_password, role='admin')
            db.session.add(new_admin)
            db.session.commit()
            print("Database initialized and Admin account created!")

    return app