import os
import requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from mpesa.mpesaToken import get_mpesa_token
from engine.db_storage import get_db_connection
from models.transactions.transaction import Transaction


load_dotenv()
app = Flask(__name__)


@app.route("/mpesa/withdraw", methods=["POST"])
def withdraw_to_mpesa():
    """Withdrawal request from Tarantula wallet to mpesa"""
    data = request.json()
    phone = data.get("phone")
    amount = data.get("amount")

    try:
        # check user's balance on the app first, prevent autocommit
        connection = get_db_connection()
        cursor = connection.cursor()
        connection.autocommit = False

        cursor.execute("SELECT user_id, balance FROM users WHERE phone_number = %s", (phone,))
        user = cursor.fetchone()

        # try to find the specific user that wants to withdraw the funds
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404
        
        # perform check if the user's balance is less than amount to be withdrawn
        if user[1] < amount:
            return jsonify({"success": False, "message": "Insufficient balance"}), 400
        
        while connection:
            transaction_data = []

            # deduct balance from the wallet before withdrawal
            updated_balance = user[1] - amount
            cursor.execute("UPDATE users SET balance = %s WHERE user_id = %s", (updated_balance, user[0]))
            transaction_id = Transaction.generate_transaction_id()
            
            # afterwards, update the transaction table, insert the records that took place
            updated_record = user[transaction_data]
            cursor.execute("UPDATE transactions SET transaction_id, type WHERE user_id = %s", (updated_record, transaction_id, user[0]))
            connection.commit()
            cursor.close()
            connection.close()

            transaction_data.append(updated_balance, updated_record)

        b2c_url = "https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest"
        token = get_mpesa_token()

        payload = {
            "InitiatorName": "Tarantula",
            "SecurityCredential": "",
            "CommandID": "BusinessPayment",
            "Amount": amount,
            "PartyA": os.getenv("MPESA_B2C_SHORTCODE"),
            "PartyB": phone,
            "Remarks": "Withdrawal from Tarantula",
            "QueueTimeOutURL": "https://tarantula.com/b2c/queue",
            "ResultURL": "https://tarantula.com/b2c/result",
            "Ocassion": "Withdraw from wallet"
        }
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        response = requests.post(b2c_url, json=payload, headers=headers)

        return jsonify(response.json())
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    

if __name__ == "__main__":
    app.run(debug=True, port=5002)