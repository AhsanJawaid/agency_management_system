from flask import Flask
from flask_login import LoginManager
from ..models import db, User
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', None)
    
    encoded_password = quote_plus(raw_password)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://root:{encoded_password}@localhost/agency"

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def login_user(user_id):
        return User.query.get(int(user_id))

    from app.auth.routes import auth
    app.register_blueprint(auth)

    return app