from app import db, socketio
from app.models.notification import Notification
from datetime import datetime

def create_notification(recipient_email, message, link=None):
    notif = Notification(
        recipient_email=recipient_email,
        message=message,
        link=link
    )
    db.session.add(notif)
    db.session.commit()

    socketio.emit('new_notification', {
        'email': recipient_email,
        'message': message,
        'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M')
    })