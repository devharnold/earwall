import os
from models.wallets.cashwallet import CashWallet
from apis.v1.views import app_views
from engine.db_storage import get_db_connection
from flask import Flask, jsonify, request
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

#Route to create cashwallet 
@app_views.route('/cashwallet', methods=['POST'], strict_slashes=False)
def create_wallet():
    """Route to create a wallet once a user signs up for the platform"""
    data = request.json()
    cashwallet = CashWallet(
        data['user_id'],
        data['cashwallet_id'],
        data['currency'],
        data['balance=0.0']
    )
    try:
        cashwallet.create_new_wallet()
        return jsonify({"message": "Wallet successfully created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Route to view detailed cashwallet information
@app_views.route('/cashwallet/', methods=['GET'], strict_slashes=False)
def get_wallet_data():
    """Router to fetch wallet details"""
    try:
        cashwallet = CashWallet.fetch_wallet_data()

    except Exception as e:
        return jsonify({"error": "Error"}), 500
    

#Route to view wallet transactions
@app_views.route('/cashwallets/balance/', methods=['GET'], strict_slashes=False)
def get_wallet_balance():
    try:
        