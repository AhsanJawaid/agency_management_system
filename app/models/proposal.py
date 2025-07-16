from datetime import datetime
from app.extensions import db
from app.models.user import User
from app.models.job import Jobs

class Proposal(db.Model):
    __tablename__ = 'proposal'

    id               = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_id           = db.Column(db.String(50), db.ForeignKey('jobs.job_id'), nullable=False)
    owner_email      = db.Column(db.String(255), db.ForeignKey('user.email'), nullable=False)
    bid_amount       = db.Column(db.Float, nullable=False)
    cover_letter     = db.Column(db.Text, nullable=True)
    created_at       = db.Column(db.DateTime, default=datetime.utcnow)
    status           = db.Column(
                          db.String(20), 
                          default='pending'
                       )  # pending, accepted, rejected

    # Relationships
    job       = db.relationship('Jobs', backref='proposals')
    owner     = db.relationship('User', foreign_keys=[owner_email])
