from app.utilities.ai import proposal_generator


@app.route('/generate_proposal/<job_id>', methods=['POST'])
@login_required
def generate_proposal(job_id):

    proposal = generate_proposal(prompt=f"Generate a proposal for job {job_id} for user {current_user.email}")