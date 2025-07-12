from flask import Blueprint, render_template
from app.models import db, Jobs

main = Blueprint('main', __name__)

@main.route('/')
def home():
    job_list = Jobs.query.order_by(Jobs.date_posted.desc()).all()
    return render_template('home.html', jobs=job_list)


@main.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')