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
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.sendmail(self.smtp_user, to_email, msg.as_string())
            print(f"Email successfully sent to {to_email}")
        except Exception as e:
            print(f"Failed to send email to {to_email}: e")
            raise

    def send_welcome_mail(sender_email, user_id, to_email):
        """Sends a Welcome mail to the user after signing up for our platform"""
        try:
            conn=get_db_connection()
            cursor=conn.cursor()
            cursor.execute(
                "SELECT first_name, last_name FROM users WHERE user_id=%s", (user_id)
            )
            user_id=cursor.fetchone()[0]
            conn.commit()

            subject="Welcome Aboard!"
            message_body=(
                f"Dear Client \n\n"
                f"You have successfully signed up for Tarantula. Enjoy your experience with our service\n\n"
                f"Best Regards,\n"
                f"Tarantula Team."
            )
            sender_email.send_email(to_email, subject, message_body)
            
        except Exception as e:
            conn.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            conn.close()