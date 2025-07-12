from flask import Flask
from app.models import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .models import User
from .models import db
from urllib.parse import quote_plus
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', None)

# Original password
# raw_password = os.environ.get('DB_PASS', None)
raw_password = "Admin@123!"

# Encode it
encoded_password = quote_plus(raw_password)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://root:{encoded_password}@localhost/agency"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def create_app():
    # app.config.from_pyfile('../.env', silent=True)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from .auth.routes import auth
    from .utils.decorators import role_required
    from .routes import main
    from app.proposal import proposal_bp
    from .routes.notifications import notifications_bp

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(proposal_bp)
    app.register_blueprint(notifications_bp)

    app.jinja_env.globals['role_required'] = role_required

    return app