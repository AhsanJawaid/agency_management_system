from .main import main_bp
from .auth import auth_bp
from .jobs import jobs_bp
from .projects import projects_bp
from .tasks import tasks_bp
from .users import users_bp
from .proposals  import proposals_bp

def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(jobs_bp, url_prefix='/jobs')
    app.register_blueprint(projects_bp, url_prefix='/projects')
    app.register_blueprint(tasks_bp, url_prefix='/tasks')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(proposals_bp)