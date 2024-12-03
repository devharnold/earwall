# send transaction mails file
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from models.user import User
from engine.db_storage import get_db_connection
from flask import jsonify


class EmailTransactionService:
    def __init__(self, smtp_host, smtp_port, smtp_user, smtp_password):
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

    def send_email_notification(self, to_email, subject, message_body):
        """boilerplate code to send emails of different topics"""
        msg=MIMEMultipart()
        msg['FROM']=self.smtp_user
        msg['TO']=to_email
        msg['Subject']=subject
        msg.attach(MIMEText(message_body, "plain"))

        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.sendmail(self.smtp_user, to_email, msg.as_string())
            print(f"Email successfully sent to {to_email}")
        except Exception as e:
            print(f"Failed to send email to {to_email}: e")
            raise


    """
    We want to send emails of two different topics
        1. Share funds complete
        2. Received funds
    """

    def send_sent_funds(sender_email, user_id, cashwallet_id, amount, first_name, last_name, to_email, transaction_id):
        #"""Sends email to the user, confirming about the sent funds and also providing the transaction details"""
        #subject= "Sent Funds"
        #message_body= f"Dear Client, \n\nYour transaction of {transaction_details['amount']}has been processed. \n\nThank you!"
        #email_sender.send_email(to_email, subject, message_body)

        try:
            conn=get_db_connection()
            cursor=conn.cursor()
            cursor.execute(
                "SELECT first_name, last_name FROM users WHERE user_id=%s", (user_id)
            )
            user_id=cursor.fetchone()[0]
            conn.commit()

            cursor.execute(
                "SELECT balance FROM cash_wallets WHERE cashwallet_id=%s", (cashwallet_id)
            )
            cashwallet_id = cursor.fetchone()
            conn.commit()

            cursor.execute(
                "SELECT transaction_id FROM transactions WHERE wallet_id=%s", (cashwallet_id, transaction_id)
            )

            subject="Payment Successful"
            message_body=(
                f"Dear Client \n\n"
                f"Your payment of {amount} to {first_name, last_name} has successfully been transacted.\n"
                f"Receipt Details: \n"
                f" - Amount: {amount}\n"
                f" - Transaction ID: {transaction_id}\n\n"
                f"Thank you for using our services \n\n"
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

    def send_received_funds(sender_email, first_name, amount, last_name, balance, user_id, cashwallet_id, transaction_id, to_email):
        """function to notify user about received funds"""
        try:
            conn=get_db_connection()
            cursor=conn.cursor()

            cursor.execute("SELECT first_name, last_name FROM users WHERE user_id=%s", (user_id))
            user_id=cursor.fetchone()
            conn.commit()

            cursor.execute("SELECT balance FROM cash_wallets WHERE wallet_id=%s", (cashwallet_id))
            cashwallet_id=cursor.fetchone()
            conn.commit()

            cursor.execute("SELECT amount FROM transactions WHERE transaction_id=%s", (transaction_id))
            transaction_id=cursor.fetchone()
            conn.commit()

            subject="Credited Funds"
            message_body=(
                f"Dear User, \n\n"
                f"You have received funds from {first_name, last_name}.\n\n"
                f"Details of the transaction:\n"
                f" - Amount: {amount}\n"
                f" - Transaction ID: {transaction_id}\n\n"
                f" - Current Balance: {balance}\n\n"
                f"Thank you for using our services.\n\n"
                f"Best Regards,\n"
                f"Tarantula Team"
            )
            sender_email.send_email(to_email, subject, message_body)

        except Exception as e:
            conn.rollback()
            return jsonify({"error": (e)}), 500
        finally:
            conn.close()
            cursor.close()

    def send_mpesa_app(sender_email, to_email, user_id, amount, transaction_id, wallet_id):
        """Sends email notification to the user after funds transfer from Mpesa to the app"""
        try:
            conn=get_db_connection()
            cursor=conn.cursor()

            cursor.execute(
                "SELECT user_id FROM cash_wallets WHERE wallet_id=%s" (user_id, wallet_id)
            )
            user_id=cursor.fetchone()
            conn.commit()

            cursor.execute(
                "SELECT amount FROM transactions WHERE transaction_id=%s" (amount, transaction_id)
            )
            transaction_id=cursor.fetchone()
            conn.commit()

            subject="Transaction Alert!"
            message_body=(
                f"Dear Client,\n"
                f"{amount} has been credited to your wallet {wallet_id} from mpesa\n\n"
                f"Tarantula Team."
            )
            sender_email.send_email(to_email, subject, message_body)

        except Exception as e:
            conn.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            conn.close()