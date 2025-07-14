from flask import Blueprint, request, jsonify
from app.models import OpportunityNotification, DailyDigest, db

notifications = Blueprint('notifications', __name__)

@notifications.route('/notify/opportunity', methods=['POST'])
def notify_opportunity():
    # TODO: Implement feasibility analysis, email sending, and DB logging
    return jsonify({'status': 'not implemented'}), 501

@notifications.route('/notify/daily-digest', methods=['POST'])
def send_daily_digest():
    # TODO: Implement daily digest summary and notification
    return jsonify({'status': 'not implemented'}), 501

@notifications.route('/notify')
def notify_home():
    return "Notifications endpoint working!"