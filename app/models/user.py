from flask_login import UserMixin
from app.extensions import db

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

    def get_id(self):
        return self.email
    
    def __repr__(self):
        return f"<User {self.email}>"

    @property
    def role(self):
        rel = Relationship.query.filter_by(user_email=self.email).first()
        return rel.role if rel else None
    
    def is_active(self):
        rel = Relationship.query.filter_by(user_email=self.email).first()
        return rel.status == "active" if rel else False

class Relationship(db.Model):
    __tablename__ = 'relationships'

    user_email = db.Column(db.String(255), db.ForeignKey('user.email'), primary_key=True)
    manager_email = db.Column(db.String(255), db.ForeignKey('user.email'))
    role = db.Column(db.String(50))
    status = db.Column(db.String(50))

    user = db.relationship('User', foreign_keys=[user_email], backref='roles')
    manager = db.relationship('User', foreign_keys=[manager_email], backref='managed_users')

def get_user_role(email):
    from app.models.user import Relationship
    rel = Relationship.query.filter_by(user_email=email).first()
    return rel.role if rel else None