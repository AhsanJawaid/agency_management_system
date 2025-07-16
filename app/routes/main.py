from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.job import Jobs
from app.models.project import Project
from app.models.task import Task
from sqlalchemy import or_

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    job_list = Jobs.query.order_by(Jobs.date_posted.desc()).all()
    return render_template('index.html', jobs=job_list)

@main_bp.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@main_bp.route('/dashboard')
@login_required
def dashboard():
    jobs_count = Jobs.query.count()
    projects_count = Project.query.filter(Project.owner_email == current_user.email).count()
    tasks_count   = Task.query.count()
    tasks_count = Task.query.filter(
            or_(
                Task.owner_email == current_user.email,
                Task.assigned_to_email == current_user.email
            )
        ).count()

    return render_template(
        'main/dashboard.html',
        jobs_count=jobs_count,
        projects_count=projects_count,
        tasks_count=tasks_count
    )