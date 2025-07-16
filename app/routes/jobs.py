from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.extensions import db
from app.models.job import Jobs
from app.forms.job_form import JobForm

jobs_bp = Blueprint('jobs', __name__, url_prefix='/jobs')

@jobs_bp.route('/')
@login_required
def list_jobs():
    all_jobs = Jobs.query.all()
    return render_template('jobs/list.html', jobs=all_jobs)

@jobs_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_job():
    form = JobForm()
    if form.validate_on_submit():
        data = {**form.data}
        data.pop('submit', None)
        data.pop('csrf_token', None)

        job = Jobs(**data)
        db.session.add(job)
        db.session.commit()
        flash("Job created!")
        return redirect(url_for('jobs.list_jobs'))
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