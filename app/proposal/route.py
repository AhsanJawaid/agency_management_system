from flask import Blueprint, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Proposal, db
from datetime import date

proposal_bp = Blueprint('proposal', __name__, url_prefix='/proposal')

@proposal_bp.route('/submit/<job_id>')
@login_required
def submit_proposal(job_id):
    # Optional: check if proposal already exists
    existing = Proposal.query.filter_by(owner_email=current_user.email, job_id=job_id).first()
    if existing:
        flash("You've already submitted a proposal for this job.")
        return redirect(url_for('main.home'))

    new_proposal = Proposal(owner_email=current_user.email, job_id=job_id, date=date.today())
    db.session.add(new_proposal)
    db.session.commit()
    flash("Proposal submitted successfully!")
    return redirect(url_for('main.home'))
