import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from backend.engine.db_storage import get_db_connection
from backend.models.user import User
from flask import jsonify

class EmailCreditWallet:
    def __init__(self, smtp_host, smtp_port, smtp_user, smtp_password):
        load_dotenv()
        """Initializes with smtp server details
        Args:
            smtp_host (str): The smtp server host
            smtp_port (str): The smtp server port
            smtp_user (str): The sender's email address
            smtp_password (str): sender's email password or app-specific password
        """
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password

        smtp_host = os.getenv("SMTP_HOST")
        smtp_port = os.getenv("SMTP_PORT")
        smtp_user = os.getenv("SMTP_USER")
        smtp_password = os.getenv("SMTP_PASSWORD")

    def send_email(self, user_email, subject, message_body):
        """boilerplate code to send emails of different topics"""
        user_email = User.find_user_by_email()
        if not user_email:
            print(f"Email not found")
        msg=MIMEMultipart()
        msg['FROM']=self.smtp_user
        msg['TO']=user_email
        msg['Subject']=subject
        msg.attach(MIMEText(message_body, "plain"))

        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.sendmail(self.smtp_user, user_email, msg.as_string())
            print(f"Email successfully sent to {user_email}")
        except Exception as e:
            print(f"Failed to send email to {user_email}: e")
            raise

    def credit_wallet_app(smtp_user, user_email, user_id, amount, transaction_id, wallet_id):
        """Sends email notification to the user after funds transfer from Mpesa to the app"""
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            cursor.execute(
                "SELECT user_id FROM wallets WHERE wallet_id=%s" (user_id, wallet_id)
            )
            user_id=cursor.fetchone()
            connection.commit()

            cursor.execute(
                "SELECT amount FROM transactions WHERE transaction_id=%s" (amount, transaction_id)
            )
            transaction_id=cursor.fetchone()
            connection.commit()

            subject="Transaction Alert!"
            message_body=(
                f"Dear Client,\n"
                f"{amount} has been successfully credited to your wallet {wallet_id} from mpesa\n\n"
                f"Tarantula Team."
            )
            smtp_user.send_email_notification(user_email, subject, message_body)

        except Exception as e:
            connection.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            connection.close()
