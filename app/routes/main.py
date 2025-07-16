# from flask import Blueprint, render_template
# from app.models import Jobs

# main = Blueprint('main', __name__)

# @main.route('/')
# def home():
#     return render_template('home.html')
#     # return "Hello from Main!"

# @main.route('/dashboard')
# def dashboard():
#     jobs = Jobs.query.all()
#     return render_template('dashboard.html', jobs=jobs)

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models import db, Project, Task, Jobs, User
from datetime import date

main = Blueprint('main', __name__)

@main.route('/')
def home():
    job_list = Jobs.query.order_by(Jobs.date_posted.desc()).all()
    return render_template('home.html', jobs=job_list)


@main.route('/dashboard')
@login_required
def dashboard():
    projects = Project.query.filter_by(owner_email=current_user.email).all()
    tasks = Task.query.filter_by(owner_email=current_user.email).all()
    jobs = Jobs.query.all()
    return render_template('dashboard.html', projects=projects, tasks=tasks, jobs=jobs)

@main.route('/jobs')
@login_required
def jobs():
    jobs = Jobs.query.all()
    return render_template('jobs.html', jobs=jobs)

@main.route('/users')
@login_required
def users():
    users = User.query.all()
    return render_template('users.html', users=users)


