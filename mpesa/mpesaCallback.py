from flask import Flask, jsonify, request
from engine.db_storage import get_db_connection

app = Flask(__name__)

"""On this file, I'm supposed to update the wallet balances after successful mpesa payments to the business' account"""
"""This will only happen if a user has successfully made payment. I'll figure it out how to handle it"""

@app.route("/mpesa/callback", methods=["POST"])
def mpesa_callback():
    """Handles mpesa STK push reponse"""
    data = request.json()
    print("M-pesa callback Data:", data)

    if data.get("Body", {}).get("stkCallback", {}).get("ResultCode") == 0:
        metadata = data["Body"]["stkCallback"]["CallbackMetadata"]["Item"]
        amount = next((item["Value"] for item in metadata if item["Name"] == "Amount"), None)
        phone = next((item["Value"] for item in metadata if item["Name"] == "Phone"), None)
        receipt = next((item["Value"] for item in metadata if item["Name"] == "MpesaReceiptNumber"), None)

        print(f"Payment recieved: {amount} from {phone}, Reciept: {receipt}")

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT user_id, balance FROM users WHERE phone_number = %s", (phone,))
            user = cursor.fetchone()

            while user:
                # create an empty list to add transaction data
                transaction_data = []

                updated_balance = user[1] + amount
                cursor.execute("UPDATE users SET balance = %s WHERE user_id = %S", (updated_balance, user[0]))
                connection.commit()
                message = f"Wallet balance updated: New balance = {updated_balance}"

                transaction_data.append(updated_balance)

                cursor.close()
                connection.close()
                return jsonify({"Success": True, "message": message})
        except Exception as e:
            return jsonify({"Success": False, "message": str(e)}), 500
        
    print("Transaction failed:", data.get("Body", {}).get("stkCallback", {}).get("ResultDesc"))
    return jsonify({"success": False, "message": "Transaction Failed"}), 400


if __name__ == "__main__":
    app.run(debug=True, port=5001)