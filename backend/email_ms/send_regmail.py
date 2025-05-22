# sending regular mail messages

import os
import smtplib
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from backend.models.user import User
from backend.engine.db_storage import get_db_connection
from flask import jsonify

class RegularEmailService:
    """Initialize the smtp server details
    Params:
        - smtp_port: The smtp server port
        - smtp_host: The smtp server host
        - smtp_user: The senders email address
        - smtp_password: The senders email password or app-specific password
    """
    def __init__(self, smtp_host, smtp_port, smtp_user, smtp_password):
        load_dotenv()
        self.smtp_port = smtp_port
        self.smtp_host = smtp_host
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password

        smtp_host = os.getenv("SMTP_HOST")
        smtp_port = os.getenv("SMTP_PORT")
        smtp_user = os.getenv("SMTP_USER")
        smtp_password = os.getenv("SMTP_PASSWORD")

    def send_email_notification(self, user_email, user_id, subject, messsage_body):
        """Function to send email notification through the smtp service to a user"""
        user_email = User.find_user_by_email()
        if not user_email:
            print(f"Email missing or user with id:{user_id} not found")
        msg=MIMEMultipart()
        msg['From'] = self.smtp_user
        msg['To'] = user_email
        msg['Subject'] = subject
        msg.attach(MIMEText(messsage_body, "plain"))

        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.sendmail(self.smtp_user, user_email, msg.as_string())
            print(f"Email successfully sent to {user_email}")
        except Exception as e:
            print(f"Failed to send email to {user_email}: e")
            raise

    def send_welcome_mail(smtp_user, user_id, user_email):
        # Sends a Welcome mail to the user after signing up for our platform
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(
                "SELECT first_name, last_name FROM users WHERE user_id=%s", (user_id)
            )
            user_id=cursor.fetchone()[0]
            connection.commit()

            subject="Welcome Aboard!"
            message_body=(
                f"Dear Client \n\n"
                f"You have successfully signed up for Tarantula. Enjoy your experience with our service\n\n"
                f"Best Regards,\n"
                f"Tarantula Team."
            )
            smtp_user.send_email_notification(user_email, subject, message_body)
            
        except Exception as e:
            connection.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            connection.close()

    def send_password_reset_email(smtp_user, first_name, last_name, user_id, user_email):
        # Sends an email notification to a user after a password update
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT first_name, last_name FROM users WHERE user_id=%s", (user_id))
            first_name=cursor.fetchone()[0]
            last_name=cursor.fetchone()[0]

            connection.commit()

            subject="Password Reset"
            message_body = (
                f"Dear {first_name} {last_name}\n\n"
                f"You have successfully reset your password. Do not share your credentials with others\n\n"
                f"Tarantula Team."
            )
            smtp_user.send_email_notification(user_email, subject, message_body)
        except Exception as e:
            connection.rollback()
            return jsonify({"Error": str(e)}), 500
        finally:
            cursor.close()
            connection.close()