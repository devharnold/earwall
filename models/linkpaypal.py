from flask import request, jsonify
import psycopg2
import paypalrestsdk
import requests

class PaypalConfig:
    paypalrestsdk.configure({
    "mode": "sandbox",
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET"
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
                "return_url": "http://yourapp.com/execute-payment",
                "cancel_url": "http://yourapp.com/cancel"
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