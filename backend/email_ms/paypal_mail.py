# sends email after successful interactions with the paypal account

import os
import smtplib
import dotenv
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from backend.models.user import User
from backend.engine.db_storage import get_db_connection
from flask import jsonify

class EmailPaypalInteractions:
    def __init__(self, smtp_user, smtp_port, smtp_host, smtp_password):
        load_dotenv()
        """smtp server details"""
        self.smtp_user = smtp_user
        self.smtp_port = smtp_port
        self.smtp_host = smtp_host
        self.smtp_password = smtp_password

        smtp_user = os.getenv("SMTP_USER")
        smtp_port = os.getenv("SMTP_PORT")
        smtp_host = os.getenv("SMTP_HOST")
        smtp_password = os.getenv("SMTP_PASSWORD")

    def get_user_email(user_id):
        """Retrieve user_email from db using user_id"""
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT user_email FROM users WHERE user_id=%s", (user_id,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()

        return result[0] if result else None

    def send_email_notification(self, user_id, subject, message_body):
        """Function to send email notification throught the smtp service to a user"""
        user_email = self.get_user_email(user_id)
        if not user_email:
            print(f"Email missing or user with id: {user_id} not found!")
            return

        msg=MIMEMultipart()
        msg['From'] = self.smtp_user
        msg['To'] = user_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message_body, "plain"))

        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.sendmail(self.smtp_user, user_email, msg.as_string())
            print(f"Email sent to {user_email}")
        except Exception as e:
            print(f"Failed to send email to {user_email}: e")
