from flask import Blueprint, render_template, redirect, url_for, jsonify
from app.models.notification import Notification
from flask_login import current_user
from app import db

notifications_bp = Blueprint('notifications', __name__, url_prefix='/notifications')

@notifications_bp.route('/')
def list_notifications():
    notifs = Notification.query.filter_by(recipient_email=current_user.email)\
                               .order_by(Notification.created_at.desc()).all()
    return render_template('notifications/list.html', notifs=notifs)

@notifications_bp.route('/<int:id>/read')
def mark_as_read(id):
    notif = Notification.query.get_or_404(id)
    notif.is_read = True
    db.session.commit()
    return redirect(url_for('notifications.list_notifications'))

@notifications_bp.route('/unread')
def unread_notifications():
    notifs = Notification.query.filter_by(
        recipient_email=current_user.email,
        is_read=False
    ).order_by(Notification.created_at.desc()).limit(10).all()

    data = [{
        'id': n.id,
        'message': n.message,
        'timestamp': n.created_at.strftime('%Y-%m-%d %H:%M')
    } for n in notifs]

    return jsonify(data)