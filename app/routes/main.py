from flask import Blueprint, render_template
from app.models import Jobs

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')
    # return "Hello from Main!"

@main.route('/dashboard')
def dashboard():
    jobs = Jobs.query.all()
    return render_template('dashboard.html', jobs=jobs)