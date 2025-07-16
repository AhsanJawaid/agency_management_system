from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.models.job import Jobs
from app.models.project import Project
from app.models.proposal import Proposal
from app.models.task import Task
from sqlalchemy import or_, func, case
from app.extensions import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    q = request.args.get('q', '').strip()
    jobs = Jobs.query

    if q:
        jobs = jobs.filter(
            Jobs.title.ilike(f'%{q}%') |
            Jobs.description.ilike(f'%{q}%') |
            Jobs.skills_requested.ilike(f'%{q}%')
        )

    jobs.order_by(Jobs.date_posted.desc()).all()
    # job_list = Jobs.query.order_by(Jobs.date_posted.desc()).all()
    return render_template('index.html', jobs=jobs, q=q)

@main_bp.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@main_bp.route('/dashboard')
@login_required
def dashboard():
    jobs_count = Jobs.query.filter(Jobs.stage != 'completed').count()
    projects_count = Project.query.filter(Project.owner_email == current_user.email).count()
    # tasks_count   = Task.query.count()
    tasks_count = Task.query.filter(
            or_(
                Task.owner_email == current_user.email,
                Task.assigned_to_email == current_user.email
            )
        ).count()

    # Proposal status breakdown
    proposals_raw = (
        db.session.query(Proposal.status, func.count(Proposal.id).label('count'))
        .group_by(Proposal.status)
        .all()
    )
    proposals = [{'status': status, 'count': count} for status, count in proposals_raw]

    # Task status breakdown
    tasks_raw = (
        db.session.query(
            case(
                (Task.completed_datetime.isnot(None), 'Completed'),
                (Task.deadline_datetime > func.now(), 'In Progress'),
                    else_='To Do').label('status'),
                    func.count(Task.task_id)
        )
        .group_by('status')
        .all()
    )
    tasks = [{'status': status, 'count': count} for status, count in tasks_raw]

    # Financial totals
    financials = (
        db.session.query(
            func.coalesce(func.sum(Jobs.expected_cost), 0).label('total_cost'),
            func.coalesce(func.sum(Jobs.expected_earning), 0).label('total_earning')
        )
        .first()
    )

    return render_template(
        'main/dashboard.html',
        jobs_count=jobs_count,
        projects_count=projects_count,
        tasks_count=tasks_count,
        proposals=proposals,
        tasks=tasks,
        financials={
            'total_cost': financials.total_cost,
            'total_earning': financials.total_earning
        }
    )