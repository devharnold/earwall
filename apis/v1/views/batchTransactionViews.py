from models.transactions.batch_transaction import BatchTransaction
import os
from dotenv import load_dotenv
from engine.db_storage import get_db_connection
from apis.v1.views import app_views
from flask import Flask, jsonify, request
load_dotenv()

app = Flask(__name__)

@app_views.route('/b_transaction', methods=['POST'], strict_slashes=False)
def process_transaction():
    """Route to start processing the batch transaction"""
    data = request.json()
    batch_transaction = BatchTransaction(
        data['sender_user_id'],
        data['receivers'],
        data['from_currency'],
        data['to_currency'],
        data['amount'],
        data['transaction_id']
    )
    try:
        batch_transaction.process_batch_transactions()
        return jsonify({"message": "Transaction Complete"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app_views.route('/b_transaction', methods=['GET'], strict_slashes=False)
def fetch_transaction_data():
    """Route to fetch transaction history"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        batch_transaction = BatchTransaction.fetch_transaction_data()

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()