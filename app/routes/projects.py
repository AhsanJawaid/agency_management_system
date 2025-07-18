from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models.project import Project
from app.models.job import Jobs
from app.forms.project_form import ProjectForm
from app.utils.notifications import create_notification
from app.utils.emails import send_email

projects_bp = Blueprint('projects', __name__, url_prefix='/projects')

@projects_bp.route('/')
@login_required
def list_projects():
    user_projects = Project.query.filter_by(owner_email=current_user.email).order_by(Project.created_at.desc()).all()
    return render_template('projects/list.html', projects=user_projects)

@projects_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_project():
    form = ProjectForm()
    form.job_id.choices = [(job.job_id, job.title) for job in Jobs.query.all()]

    if form.validate_on_submit():
        project = Project(
            job_id=form.job_id.data,
            owner_email=current_user.email,
            title=form.title.data,
            description=form.description.data,
            status=form.status.data
        )
        db.session.add(project)
        db.session.commit()
        flash("Project created!", "success")
        # Notify freelancer
        create_notification(
            recipient_email=project.owner_email,
            message=f"New project assigned: '{project.description}'",
            link=url_for('projects.view_project', id=project.id)
        )

        create_notification(
            recipient_email=project.owner_email,
            message=f"Project created and assigned to {project.owner_email}: '{project.description}'",
            link=url_for('projects.view_project', id=project.id)
        )

        send_email(
            subject="New Project Assigned",
            recipients=[project.owner_email],
            body_text=f"You've been assigned a new project: {project.description}",
            body_html=f"<p>New Project: <strong>{project.description}</strong></p>"
        )
        return redirect(url_for('projects.list_projects'))
    return render_template('projects/create.html', form=form)

@projects_bp.route('/<int:id>')
@login_required
def view_project(id):
    project = Project.query.get_or_404(id)
    return render_template('projects/detail.html', project=project)

@projects_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_project(id):
    project = Project.query.get_or_404(id)
    form = ProjectForm(obj=project)
    form.job_id.choices = [(job.job_id, job.title) for job in Jobs.query.all()]

    if form.validate_on_submit():
        project.job_id = form.job_id.data
        project.title = form.title.data
        project.description = form.description.data
        project.status = form.status.data
        db.session.commit()
        flash("Project updated!", "success")
        return redirect(url_for('projects.view_project', id=id))
    return render_template('projects/update.html', form=form, project=project)

@projects_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash("Project deleted.", "success")
    return redirect(url_for('projects.list_projects'))