from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_socketio import SocketIO

# Instantiate extensions
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
socketio = SocketIO(cors_allowed_origins="*")

# Optional: Configure login view
login_manager.login_view = 'auth.login'
login_manager.login_message = "You must be logged in to access this page."
login_manager.login_message_category = "warning"