from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.models.user import User, Relationship
from app.forms.login_form import LoginForm
from app.forms.signup_form import SignupForm

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print("Login form validated")
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for('main.dashboard'))
        else:
            flash("Invalid credentials.", "danger")
    else:
        print("Form did not validate:", form.errors)
    return render_template('login.html', form=form)

@users_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
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
    return render_template('signup.html', form=form)

@users_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", "success")
    return redirect(url_for('auth.login'))

@users_bp.route('/<email>')
@login_required
def view_user(email):
    user = User.query.get_or_404(email)
    return render_template('users/detail.html', user=user)