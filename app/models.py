# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer)
    email = db.Column(db.String(255), primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    password = db.Column(db.String(255))
    contact = db.Column(db.String(50))
    upwork_profile = db.Column(db.Text)
    connects_balance = db.Column(db.Integer)
    title = db.Column(db.String(255))
    hourly_rate = db.Column(db.Numeric(10, 2))
    milestone_rate = db.Column(db.Numeric(10, 2))

    def __repr__(self):
        return f"<User {self.email}>"

    @property
    def role(self):
        rel = Relationship.query.filter_by(user_email=self.email).first()
        return rel.role if rel else None
    
    def is_active(self):
        rel = Relationship.query.filter_by(user_email=self.email).first()
        return rel.status == "active" if rel else False


class Jobs(db.Model):
    __tablename__ = 'jobs'

    job_id = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    connects_required = db.Column(db.Integer)
    category = db.Column(db.String(100))
    skills_requested = db.Column(db.Text)
    date_posted = db.Column(db.Date)
    deadline = db.Column(db.Date)
    stage = db.Column(db.String(100))
    expected_cost = db.Column(db.Numeric(10, 2))
    expected_earning = db.Column(db.Numeric(10, 2))
    client_rating = db.Column(db.Numeric(3, 2))
    feasibility_score = db.Column(db.Numeric(4, 2))
    link = db.Column(db.String(255))

class Project(db.Model):
    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_id = db.Column(db.String(100), db.ForeignKey('jobs.job_id'))
    owner_email = db.Column(db.String(255), db.ForeignKey('user.email'))
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.Date, default=db.func.current_date())
    status = db.Column(db.String(50))

    # Relationships
    job = db.relationship('Jobs', backref='project')
    owner = db.relationship('User', backref='projects')


class Proposal(db.Model):
    __tablename__ = 'proposal'

    owner_email = db.Column(db.String(255), db.ForeignKey('user.email'), primary_key=True)
    job_id = db.Column(db.String(100), db.ForeignKey('jobs.job_id'), primary_key=True)
    date = db.Column(db.Date)
    status = db.Column(db.String(50), default='pending')  # e.g., 'pending', 'accepted', 'rejected'

    # Relationships
    owner = db.relationship('User', backref='proposals')
    job = db.relationship('Jobs', backref='proposals')

class SkillsDirectory(db.Model):
    __tablename__ = 'skills_directory'

    skill_version = db.Column(db.String(100), primary_key=True)
    category = db.Column(db.String(100))
    sub_category = db.Column(db.String(100))

class UserSkills(db.Model):
    __tablename__ = 'user_skills'

    email = db.Column(db.String(150), db.ForeignKey('user.email'), primary_key=True)
    skill_version = db.Column(db.String(100), db.ForeignKey('skills_directory.skill_version'), primary_key=True)
    proficiency_level = db.Column(db.String(50))  # e.g., 'beginner', 'intermediate', 'expert'
    years_of_experience = db.Column(db.Integer)

    user = db.relationship('User', backref='skills')
    skill = db.relationship('SkillsDirectory', backref='users')

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(100), db.ForeignKey('user.email'))
    message = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    is_read = db.Column(db.Boolean, default=False)

    user = db.relationship('User', foreign_keys=[user_email], backref='notifications')

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_email = db.Column(db.String(100), db.ForeignKey('user.email'))
    receiver_email = db.Column(db.String(100), db.ForeignKey('user.email'))
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    is_read = db.Column(db.Boolean, default=False)

    sender = db.relationship('User', foreign_keys=[sender_email], backref='sent_messages')
    receiver = db.relationship('User', foreign_keys=[receiver_email], backref='received_messages')


class Relationship(db.Model):
    __tablename__ = 'relationships'

    user_email = db.Column(db.String(255), db.ForeignKey('user.email'), primary_key=True)
    manager_email = db.Column(db.String(255), db.ForeignKey('user.email'))
    role = db.Column(db.String(50))
    status = db.Column(db.String(50))

    user = db.relationship('User', foreign_keys=[user_email], backref='roles')
    manager = db.relationship('User', foreign_keys=[manager_email], backref='managed_users')


def get_user_role(email):
    from app.models import Relationship
    rel = Relationship.query.filter_by(user_email=email).first()
    return rel.role if rel else None
