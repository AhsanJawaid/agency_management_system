from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
from app.models.job import Jobs
from app.models.proposal import Proposal
from app.forms.proposal_form import ProposalForm

proposals_bp = Blueprint('proposals', __name__, url_prefix='/proposals')


@proposals_bp.route('/job/<job_id>/create', methods=['GET', 'POST'])
@login_required
def submit_proposal(job_id):
    job = Jobs.query.get_or_404(job_id)
    form = ProposalForm()
    if form.validate_on_submit():
        proposal = Proposal(
            job_id=job.job_id,
            owner_email=current_user.email,
            bid_amount=form.bid_amount.data,
            cover_letter=form.cover_letter.data
        )
        db.session.add(proposal)
        db.session.commit()
        flash("Proposal submitted!")
        return redirect(url_for('proposals.list_for_job', job_id=job.job_id))
    return render_template('proposals/create.html', job=job, form=form)


@proposals_bp.route('/job/<job_id>')
@login_required
def list_for_job(job_id):
    job = Jobs.query.get_or_404(job_id)
    proposals = Proposal.query \
        .filter_by(job_id=job_id) \
        .order_by(Proposal.created_at.desc()) \
        .all()
    return render_template('proposals/list.html', job=job, proposals=proposals)


@proposals_bp.route('/<int:proposal_id>')
@login_required
def detail(proposal_id):
    proposal = Proposal.query.get_or_404(proposal_id)
    return render_template('proposals/detail.html', proposal=proposal)