# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False) # 'admin', 'manager', 'freelancer'

class Freelancer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    skills = db.Column(db.String(200))
    hourly_rate = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    client = db.Column(db.String(100))
    status = db.Column(db.String(50))  # e.g., 'active', 'completed'

class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    freelancer_id = db.Column(db.Integer, db.ForeignKey('freelancer.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    agreed_rate = db.Column(db.Float)