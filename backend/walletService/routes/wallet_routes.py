import os
from walletService.models.wallet import Wallet
from backend.apis.v1.views import app_views
from backend.engine.db_storage import get_db_connection
from flask import Flask, jsonify, request
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

#Route to create cashwallet 
@app_views.route('/', methods=['POST'])
def create_wallet():
    # create a wallet
    data = request.json()
    wallet = Wallet(
        data['user_id'],
        data['wallet_id'],
        data['currency'],
        data['balance=0.0']
    )
    try:
        wallet.create_new_wallet()
        return jsonify({"message": "Wallet successfully created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Route to view detailed cashwallet information
@app_views.route('/wallet/<int:wallet_id>', methods=['GET'])
def get_wallet_data():
    """Router to fetch wallet details"""
    try:
        wallet = Wallet.fetch_wallet_data()
        if wallet:
            return jsonify({
                "user_id": wallet.user_id,
                "balance": wallet.balance,
                "currency": wallet.currency,
                "wallet_id": wallet.wallet_id
            }), 200
        else:
            return jsonify({"error": "Wallet not found"}), 404
    except Exception as e:
        return jsonify({"error": {e}}), 500

    except Exception as e:
        return jsonify({"error": "Error"}), 500
    
