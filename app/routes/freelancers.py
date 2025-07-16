from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.user import User, Relationship
from app.forms.freelancer_form import FreelancerForm
from sqlalchemy.orm import aliased
from app.extensions import db

freelancer_bp = Blueprint('freelancers', __name__, url_prefix='/freelancers')

@freelancer_bp.route('/')
def list_freelancers():
    freelancers = (
        db.session.query(User)
        .join(Relationship, Relationship.user_email == User.email)
        .filter(Relationship.role == 'freelancer', Relationship.status == 'active')
        .all()
    )
    return render_template('freelancers/list.html', freelancers=freelancers)

@freelancer_bp.route('/<string:email>')
def view_freelancer(email):
    freelancer = (
        db.session.query(User)
        .join(Relationship, Relationship.user_email == User.email)
        .filter(User.email == email, Relationship.role == 'freelancer', Relationship.status == 'active')
        .first_or_404()
    )
    return render_template('freelancers/detail.html', freelancer=freelancer)

@freelancer_bp.route('/create', methods=['GET', 'POST'])
def create_freelancer():
    form = FreelancerForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            contact=form.contact.data,
            title=form.title.data,
            hourly_rate=form.hourly_rate.data,
            milestone_rates=form.milestone_rates.data,
            connects_balance=form.connects_balance.data,
            upwork_profile=form.upwork_profile.data,
            is_active=form.is_active.data
        )
        relationship = Relationship(
            user_email=form.email.data,
            manager_email=form.manager_email.data,
            role='freelancer',
            status='active'
        )
        db.session.add(user)
        db.session.add(relationship)
        db.session.commit()
        flash('Freelancer added successfully!', 'success')
        return redirect(url_for('freelancers.list_freelancers'))
    return render_template('freelancers/create.html', form=form)

@freelancer_bp.route('/<string:email>/edit', methods=['GET', 'POST'])
def edit_freelancer(email):
    user = User.query.get_or_404(email)
    form = FreelancerForm(obj=user)
    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.contact = form.contact.data
        user.contact = form.contact.data
        user.title = form.title.data
        user.hourly_rate = form.hourly_rate.data
        user.milestone_rates = form.milestone_rates.data
        user.connects_balance = form.connects_balance.data
        user.upwork_profile = form.upwork_profile.data
        user.is_active = form.is_active.data
        db.session.commit()
        flash('Freelancer updated!', 'success')
        return redirect(url_for('freelancers.list_freelancers'))
    return render_template('freelancers/edit.html', form=form)

@freelancer_bp.route('/<string:email>/delete', methods=['POST'])
def delete_freelancer(email):
    user = User.query.get_or_404(email)
    Relationship.query.filter_by(user_email=email, role='freelancer').delete()
    db.session.delete(user)
    db.session.commit()
    flash('Freelancer deleted!', 'danger')
    return redirect(url_for('freelancers.list_freelancers'))