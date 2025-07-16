# app/routes/notifications.py
from flask import Blueprint, render_template

notifications = Blueprint('notifications', __name__)

@notifications.route('/notifications')
def list_notifications():
    # Fetch notifications for current_user
    user_notifications = [
        {"message": "New job posted!", "time": "2 min ago"},
        {"message": "Proposal approved!", "time": "10 min ago"}
    ]
    return render_template('notifications/list.html', notifications=user_notifications)
