from datetime import datetime
from app.extensions import db

class Project(db.Model):
    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_id = db.Column(db.String(100), db.ForeignKey('jobs.job_id'))
    owner_email = db.Column(db.String(255), db.ForeignKey('user.email'))
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50))

    # Relationships
    job = db.relationship('Jobs', backref='project')
    owner = db.relationship('User', backref='projects')