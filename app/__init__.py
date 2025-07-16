from flask import Flask
from app.models import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from .models import User
from urllib.parse import quote_plus
import os
from app.models import Notification


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', None)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', None)

# Original password
raw_password = os.environ.get('DB_PASS', None)
# raw_password = "Admin@123!"

# Encode it
encoded_password = quote_plus(raw_password)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://root:{encoded_password}@localhost/agency"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def create_app():
    app.config.from_pyfile('../.env', silent=True)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_email):
        return User.query.get(user_email)

    @app.context_processor
    def inject_notifications():
        if current_user.is_authenticated:
            notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).limit(10).all()
            unread_count = Notification.query.filter_by(user_id=current_user.id, read=False).count()
        else:
            notifications = []
            unread_count = 0
        return dict(notifications=notifications, unread_notifications=unread_count)

    # Register blueprints
    from app.auth.routes import auth
    from app.utils.decorators import role_required
    from app.routes import main
    from app.proposal import proposal_bp
    from app.jobs.routes import jobs_bp
    from app.projects.routes import projects_bp
    from app.tasks.routes import tasks_bp
    from app.routes.notifications import notifications

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(proposal_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(notifications)

    app.jinja_env.globals['role_required'] = role_required

    return app