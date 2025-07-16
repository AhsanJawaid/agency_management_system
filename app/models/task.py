from datetime import datetime
from app.extensions import db

class Task(db.Model):
    __tablename__ = 'tasks'

    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_email = db.Column(db.String(255), db.ForeignKey('user.email'))
    job_id = db.Column(db.String(50), db.ForeignKey('jobs.job_id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    assigned_to_email = db.Column(db.String(255), db.ForeignKey('user.email'),)
    created_datetime = db.Column(db.DateTime, default=datetime.utcnow)
    deadline_datetime = db.Column(db.Date)
    completed_datetime = db.Column(db.Date)
    priority = db.Column(db.String(50))
    description = db.Column(db.Text)

    # relationship
    owner = db.relationship('User', foreign_keys=[owner_email])
    assignee = db.relationship('User', foreign_keys=[assigned_to_email])
    job = db.relationship('Jobs', backref='tasks')
    project = db.relationship('Project', backref='tasks')