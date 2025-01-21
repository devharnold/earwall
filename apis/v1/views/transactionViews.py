from models.transactions.transaction import Transaction
import os
from dotenv import load_dotenv
from engine.db_storage import get_db_connection
from apis.v1.views import app_views
from flask import Flask, jsonify, request
load_dotenv()

app = Flask(__name__)

@app_views.route('/transaction', methods=['POST'], strict_slashes=False)
def process_transaction():
    """Route to initiate the transaction process"""
    data = request.json()
    transaction = Transaction(
        data['sender_user_id'],
        data['receiver_user_id'],
        data['from_currency'],
        data['to_currency'],
        data['amount'],
        data['transaction_id']
    )
    try:
        transaction.process_p2p_transaction()
        return jsonify({"message": "Transaction complete"}), 200
    except Exception as e:
        return jsonify({"Error": str(e)}), 500
    
    
@app_views.route('/transaction', methods=['GET'], strict_slashes=False)
def view_transaction_history():
    """Route to fetch transactions done by the user"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        transaction = Transaction.fetch_transaction_data()
        
    except Exception as e:
        return jsonify({"Error": str(e)}), 500
    
    finally:
        cursor.close()
        connection.close()

    