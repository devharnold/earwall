from flask import Flask, request, jsonify
import paypalrestsdk
import dotenv
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()

class PaypalConfig:
    paypalrestsdk.configure({
    "mode": "sandbox",
    "client_id": os.getenv("PAYPAL_CLIENT_ID"),
    "client_secret": os.getenv("PAYPAL_CLIENT_SECRET")
    })

    def create_payment(amount, currency, recipient_email):
        payment = paypalrestsdk.Payment({
            "intent": "payment",
            "payer": {
                "payment_method": "paypal"
            },
            "transactions": [{
                "amount": {
                    "total": str(amount),
                    "currency": currency
                },
                "payee": {
                    "email": recipient_email
                },
                "description": "Payment description"
            }],
            "redirect_urls": {
                "return_url": "http://localhost:3000/execute-payment",
                "cancel_url": "http://localhost:3000/cancel"
            }
        })

        if payment.create():
            print("Payment created successfully.")
            for link in payment.links:
                if link.rel == "approval_url":
                    return link.href
        else:
            return {"error": payment.error}
    
    def execute_payment(payment_id, payer_id):
        payment = paypalrestsdk.Payment.find(payment_id)

        if payment.execute({"payer_id": payer_id}):
            print("Payment executed successfully")
            return {"message": "Payment Completed"}
        else:
            return {"error": payment.error}
        

if __name__ == "__main__":
    app.run(debug=True)