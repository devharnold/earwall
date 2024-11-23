# sending regular mail messages

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from models.user import User
from engine.db_storage import get_db_connection
from flask import jsonify


class RegularEmailService:
    """Initialize the smtp server details
    Params:
        - smtp_port: The smtp server port
        - smtp_host: The smtp server host
        - smtp_user: The senders email address
        - smtp_password: The senders email password or app-specific password"""
    def __init__(self, smtp_host, smtp_port, smtp_user, smtp_password):
        self.smtp_port = smtp_port
        self.smtp_host = smtp_host
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password

    def send_email_notification(self, to_email, subject, messsage_body):
        """Function to send email notification through the smtp service to a user"""
        msg=MIMEMultipart()
        msg['FROM']=self.smtp_user
        msg['TO']=to_email
        msg['SUBJECT']=subject
        msg.attach(MIMEText(messsage_body, "plain"))

        try:
            with smtplib.SMTP(self.smtp_host, )

