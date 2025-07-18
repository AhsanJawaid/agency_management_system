from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.models.user import User, Relationship
from app.extensions import db, login_manager
from app.forms.login_form import LoginForm
from app.forms.signup_form import SignupForm
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@login_manager.user_loader
def load_user(email):
    return User.query.get(email)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(form.email.data)
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for('main.dashboard'))
        else:
            flash("Invalid credentials.", "danger")
    return render_template('auth/login.html', form=form)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        if User.query.get(form.email.data):
            flash("Email already registered.", "warning")
        else:
            hashed_pw = generate_password_hash(form.password.data)
            user = User(
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                contact=form.contact.data,
                password=hashed_pw,
                connects_balance=20,
                title="New User",
                hourly_rate=25.0,
                milestone_rate=100.0
            )
            db.session.add(user)

            rel = Relationship(
                user_email=form.email.data,
                manager_email=None,
                role=form.role.data,
                status="active"
            )
            db.session.add(rel)
            db.session.commit()
            flash("Account created! Please log in.", "success")
            return redirect(url_for('auth.login'))
    return render_template('auth/signup.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You’ve been logged out.", "success")
    return redirect(url_for('auth.login'))
