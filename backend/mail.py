# mail.py

import smtplib
from email.mime.text import MIMEText

SMTP_HOST = 'localhost'
SMTP_PORT = 1025
FROM_ADDRESS = 'admin@ppa.com'


def send_email(to_address, subject, message, is_html=False):
    msg_type = 'html' if is_html else 'plain'
    msg = MIMEText(message, msg_type)
    msg['Subject'] = subject
    msg['From'] = FROM_ADDRESS
    msg['To'] = to_address

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.send_message(msg)
        print(f"Email sent to {to_address}!")
    except smtplib.SMTPException as e:
        print(f"Error sending email: {e}")
