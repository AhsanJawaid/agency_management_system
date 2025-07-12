from flask import Blueprint, render_template, redirect, url_for, request
from app.models import Freelancer
from app.utils.decorators import role_required
from ..models import db

freelancers_bp = Blueprint('freelancers', __name__, url_prefix='/freelancers')

@freelancers_bp.route('/')
@role_required('admin', 'manager', 'freelancer')
def list_freelancers():
    freelancers = Freelancer.query.all()
    return render_template('freelancers/list.html', freelancers=freelancers)


@freelancers_bp.route('/add', methods=['GET', 'POST'])
@role_required('admin', 'manager')
def add_freelancer():
    if request.method == 'POST':
        name = request.form['name']
        skills = request.form['skills']
        rate = request.form['rate']
        freelancer = Freelancer(name=name, skills=skills, hourly_rate=rate)
        db.session.add(freelancer)
        db.session.commit()
        return redirect(url_for('list_freelancers'))
    return render_template('freelancers/add.html')