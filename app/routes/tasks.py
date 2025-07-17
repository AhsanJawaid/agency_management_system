from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models.user import User
from app.models.job import Jobs
from app.models.task import Task
from app.models.project import Project
from app.forms.task_form import TaskForm
from app.utils.notifications import create_notification
from app.utils.emails import send_email

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@tasks_bp.route('/')
@login_required
def list_tasks():
    tasks = Task.query.filter_by(owner_email=current_user.email).all()
    return render_template('tasks/list.html', tasks=tasks)

@tasks_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_task():
    form = TaskForm()
    # form.job_id.choices = [(job.job_id, job.title) for job in Jobs.query.all()]
    form.job_id.choices = [
        (job.job_id, job.title)
        for job in Jobs.query.join(Project).filter(Project.job_id == Jobs.job_id).distinct().all()
    ]

    form.assigned_to_email.choices = [(user.email, user.first_name) for user in User.query.all()]
    form.project_id.choices = [(p.id, p.title) for p in Project.query.all()]

    if form.validate_on_submit():
        task = Task(
            owner_email=current_user.email,
            job_id=form.job_id.data,
            project_id=form.project_id.data,
            assigned_to_email=form.assigned_to_email.data,
            deadline_datetime=form.deadline_datetime.data,
            priority=form.priority.data,
            description=form.description.data
        )
        db.session.add(task)
        db.session.commit()
        flash("Task created!")
        # Notify freelancer
        create_notification(
            recipient_email=task.assigned_to_email,
            message=f"New task assigned: '{task.description}' with priority {task.priority}",
            link=url_for('tasks.view_task', task_id=task.task_id)
        )

        create_notification(
            recipient_email=task.owner_email,
            message=f"Task created and assigned to {task.assigned_to_email}: '{task.description}'",
            link=url_for('tasks.view_task', task_id=task.task_id)
        )

        # send_email(
        #     subject="New Task Assigned",
        #     recipients=[task.assigned_to_email],
        #     body_text=f"You've been assigned a new task: {task.description}",
        #     body_html=f"<p>New task: <strong>{task.description}</strong><br>Deadline: {task.deadline_datetime}</p>"
        # )
        return redirect(url_for('tasks.list_tasks'))
    return render_template('tasks/create.html', form=form)


@tasks_bp.route('/<int:task_id>')
@login_required
def view_task(task_id):
    task = Task.query.get_or_404(task_id)
    return render_template('tasks/detail.html', task=task)


@tasks_bp.route('/<int:task_id>/update', methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    form = TaskForm(obj=task)
    form.job_id.choices = [(j.job_id, j.title) for j in Jobs.query.all()]
    form.project_id.choices = [(p.id, p.title) for p in Project.query.all()]
    form.assigned_to_email.choices = [(u.email, u.first_name) for u in User.query.all()]

    if form.validate_on_submit():
        task.job_id = form.job_id.data
        task.project_id = form.project_id.data
        task.assigned_to_email = form.assigned_to_email.data
        task.deadline_datetime = form.deadline_datetime.data
        task.priority = form.priority.data
        task.description = form.description.data
        db.session.commit()
        flash("Task updated successfully!")
        return redirect(url_for('tasks.view_task', task_id=task_id))

    return render_template('tasks/update.html', form=form, task=task)


@tasks_bp.route('/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted successfully!")

    return redirect(url_for('tasks.list_tasks'))


@tasks_bp.route('/projects-by-job/<job_id>')
@login_required
def projects_by_job(job_id):
    from flask import jsonify
    projects = Project.query.filter_by(job_id=job_id).all()
    project_options = [{'id': p.id, 'title': p.title} for p in projects]
    return jsonify(project_options)