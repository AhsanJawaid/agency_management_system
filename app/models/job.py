from datetime import datetime
from app.extensions import db

class Jobs(db.Model):
    __tablename__ = 'jobs'

    job_id = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    connects_required = db.Column(db.Integer)
    category = db.Column(db.String(100))
    skills_requested = db.Column(db.Text)
    date_posted = db.Column(db.Date, default=datetime.utcnow)
    deadline = db.Column(db.Date)
    stage = db.Column(db.String(100))
    expected_cost = db.Column(db.Numeric(10, 2))
    expected_earning = db.Column(db.Numeric(10, 2))
    client_rating = db.Column(db.Numeric(3, 2))
    feasibility_score = db.Column(db.Numeric(4, 2))
    link = db.Column(db.String(255))