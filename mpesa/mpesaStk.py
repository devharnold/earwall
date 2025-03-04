import os
import requests
import base64
from datetime import datetime
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from mpesaToken import get_mpesa_token

load_dotenv()
app = Flask(__name__)

@app.route("/mpesa/stkpush", methods=["POST"])
def stk_push():
    """Initiate stk push request to mpesa"""
    data = request.json()
    phone = data.get("phone")
    amount = data.get("amount")

    shortcode = os.getenv("MPESA_SHORTCODE")
    passkey = os.getenv("MPESA_PASSKEY")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password = base64.b64encode(f"{shortcode}{passkey}{timestamp}".encode()).decode()

    stk_push_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": shortcode,
        "PhoneNumber": phone,
        "CallBackURL": os.getenv("MPESA_CALLBACK_URL"),
        "AccountReference": "Tarantula",
        "TransactionDesc": "Deposit to wallet"
    }

    try:
        token = get_mpesa_token()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        response = requests.post(stk_push_url, json=payload, headers=headers)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# should put this block of code inside a function
# for cancelled transactions url
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer u6FbZPSjxZUP3RkiyELcNsAxDkcG'
}
payload = {
    "ShortCode": 600977,
    "ResponseType": "Cancelled",
    "ConfirmationURL": "https://mydomain.com/confirmation",
    "ValidationURL": "https://mydomain.com/validation",
  }
response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl', headers = headers, data = payload)
print(response.text.encode('utf8'))
    
if __name__ == "__main__":
    app.run(debug=True, port=5000)



# structure of the confirmation and validation result:
#  "TransactionType": "Pay Bill",
#  "TransID":"RKTQDM7W6S",
#  "TransTime":"20191122063845",
#  "TransAmount":"10"
#  "BusinessShortCode": "600638",
#  "BillRefNumber":"invoice008",
#  "InvoiceNumber":"",
#  "OrgAccountBalance":""
#  "ThirdPartyTransID": "",
#  "MSISDN":"25470****149",
#  "FirstName":"John",
#  "MiddleName":""
#  "LastName":"Doe"