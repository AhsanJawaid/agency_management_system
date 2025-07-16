from flask import Flask, render_template
from app.extensions import db, login_manager, mail
from app.routes import register_blueprints

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    register_blueprints(app)
    return app