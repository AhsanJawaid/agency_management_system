from flask import Blueprint, request, jsonify, current_app
from app.models import OpportunityNotification, DailyDigest, db
from flask_mail import Message


notifications = Blueprint('notifications', __name__)

@notifications.route('/notify/opportunity', methods=['POST'])
def notify_opportunity():
    # TODO: Implement feasibility analysis, email sending, and DB logging
    data = request.get_json()

    if not data or 'opportunity_id' not in data or 'user_email' not in data or 'title' not in data or 'description' not in data or 'recipients' not in data:
        return jsonify({'status': 'not implemented'}), 501
    
    opportunity_id = data['opportunity_id']
    user_email = data['user_email']
    title = data['title']
    description = data['description']
    recipients = data['recipients']

    try:
        msg = Message(subject=f"New Opportunity: {title}",
                     sender=current_app.config['MAIL_DEFAULT_SENDER'],
                     recipients=recipients,
                     body=f"Opportunity Dexcription: {description}\n\n").mail.send(msg)
        
        notification = OpportunityNotification(
            opportunity_id=opportunity_id,
            user_email=user_email,
            title=title,
            description=description,
            recipients=",".join(recipients)
        )
        db.session.add(notification)
        db.session.commit()

        return jsonify({'status': 'Opportunity notification sent'}), 200

    except Exception as e:
        current_app.logger.error(f"Error sending opportunity email: {e}")
        return jsonify({'error': 'Failed to send opportunity notification'}), 500

@notifications.route('/notify/daily-digest', methods=['POST'])
def send_daily_digest():
    # TODO: Implement daily digest summary and notification
    data=request.get_json()

    if not data or 'user_email' not in data or 'summary' not in data or 'recipients' not in data:
        return jsonify({'status': 'not implemented'}), 501
    
    user_email = data['user_email']
    summary = data['summary']
    recipients = data['recipients']

    try:
        msg = Message(subject="Daily Digest Summary",
                      sender=current_app.config['MAIL_DEFAULT_SENDER'],
                      recipients=recipients,
                      body=f"Daily Summary:\n\n{summary}").mail.send(msg)
        
        digest = DailyDigest(
            user_email=user_email,
            summary=summary,
            recipients=",".join(recipients)
        )
        db.session.add(digest)
        db.session.commit()

        return jsonify({'status': 'Daily digest sent'}), 200
    
    except Exception as e:
        current_app.logger.error(f"Error sending daily digest email: {e}")
        return jsonify({'error': 'Failed to send daily digest'}), 500
    
@notifications.route('/notify')
def notify_home():
    return "Notifications endpoint working!"