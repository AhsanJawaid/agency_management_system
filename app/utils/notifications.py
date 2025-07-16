from app import db
from app.models.notification import Notification

def create_notification(recipient_email, message, link=None):
    notif = Notification(
        recipient_email=recipient_email,
        message=message,
        link=link
    )
    db.session.add(notif)
    db.session.commit()