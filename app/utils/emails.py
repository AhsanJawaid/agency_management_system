from flask_mail import Message
from app import mail

def send_email(subject, recipients, body_html=None, body_text=None):
    msg = Message(subject, recipients=recipients)
    if body_text:
        msg.body = body_text
    if body_html:
        msg.html = body_html
    mail.send(msg)