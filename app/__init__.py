from flask import Flask
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
    app.config.from_pyfile('../.env', silent=True)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth.routes import auth
    app.register_blueprint(auth)
    from .utils.decorators import role_required
    app.jinja_env.globals['role_required'] = role_required
    from .routes import main
    app.register_blueprint(main)

    from app.freelancers.routes import freelancers_bp
    app.register_blueprint(freelancers_bp)

    return app