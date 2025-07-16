from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import db, Jobs, Notification
from .forms import JobForm
from sqlalchemy.inspection import inspect

jobs_bp = Blueprint('jobs', __name__, url_prefix='/jobs')

@jobs_bp.route('/')
@login_required
def list_jobs():
    jobs = Jobs.query.all()
    return render_template('jobs/list.html', jobs=jobs)

@jobs_bp.route('/jobs_bp/create', methods=['GET', 'POST'])
@login_required
def create_job():
    form = JobForm()
    if form.validate_on_submit():
        print("Form validated")
        try:
            model_columns = set(c.key for c in inspect(Jobs).mapper.column_attrs)
            job_data = {field: value for field, value in form.data.items() if field in model_columns}
            # job_data['created_by'] = current_user.id

            new_job = Jobs(**job_data)
            db.session.add(new_job)
            db.session.commit()
            notification = Notification(
                user_id=current_user.id,  # Could be current user or admin
                message=f"New job created: {form.title.data}"
            )
            db.session.add(notification)
            db.session.commit()

            flash('Job created successfully!', 'success')
            return redirect(url_for('jobs.list_jobs'))

        except Exception as e:
            db.session.rollback()
            print("Error during DB commit:", e)
            flash(f'Error creating job: {str(e)}', 'danger')
    else:
        print("Validation failed:", form.errors)
    return render_template('jobs/create.html', form=form)

@jobs_bp.route('/<job_id>')
@login_required
def view_job(job_id):
    job = Jobs.query.get_or_404(job_id)
    return render_template('jobs/detail.html', job=job)

@jobs_bp.route('/<job_id>/update', methods=['GET', 'POST'])
@login_required
def update_job(job_id):
    job = Jobs.query.get_or_404(job_id)
    form = JobForm(obj=job)
    if form.validate_on_submit():
        for field in form.data:
            setattr(job, field, form.data[field])
        db.session.commit()
        flash("Job updated!")
        return redirect(url_for('jobs.view_job', job_id=job_id))
    return render_template('jobs/update.html', form=form, job=job)

@jobs_bp.route('/<job_id>/delete', methods=['POST'])
@login_required
def delete_job(job_id):
    job = Jobs.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    flash("Job deleted.")
    return redirect(url_for('jobs.list_jobs'))
