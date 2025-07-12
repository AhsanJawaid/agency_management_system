from app.models import User, Relationships

@dashboard_bp.route('/freelancers')
def list_freelancers():
    freelancers = db.session.query(User).join(Relationships).filter(Relationships.role == 'freelancer').all()
    return render_template('freelancers.html', users=freelancers)
