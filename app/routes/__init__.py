from flask import Flask
from app.routes.main import main  # ✅ correct import

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)  # ✅ Blueprint object
    return app