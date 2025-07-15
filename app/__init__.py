from flask import Flask
from app.models import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .models import User
from .models import db
from urllib.parse import quote_plus
from app.routes.main import main
from app.routes.notifications import notifications
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', None)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', None)

# Original password
raw_password = os.environ.get('DB_PASS', 'Pakistan@649')
# raw_password = "Admin@123!"

 # Encode it, ensure raw_password is str
if isinstance(raw_password, bytes):
    raw_password = raw_password.decode('utf-8')
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

    # Register blueprints
    from app.auth.routes import auth
    from app.utils.decorators import role_required
    from app.routes import main
    from app.proposal import proposal_bp
    from app.routes.notifications import notifications

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(proposal_bp)
    app.register_blueprint(notifications)

    app.jinja_env.globals['role_required'] = role_required

    return app