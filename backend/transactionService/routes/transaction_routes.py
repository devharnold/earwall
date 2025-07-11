import os
import dotenv
from dotenv import load_dotenv
from flask import Flask, jsonify, request, Blueprint
from backend.engine.db_storage import get_db_connection
from transactionService.models.transaction import Transaction

app_views = Blueprint('app_views', __name__)

load_dotenv()
app = Flask(__name__)

@app_views.route('/', methods=['POST'])
def process_transaction():
    """initiate the transaction process"""
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
    
    
@app_views.route('/<int:transaction_id>/transaction', methods=['GET'])
def view_transaction_history():
    # fetch transactions done by the user
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        transaction = Transaction.fetch_transaction_history()

        if not transaction:
            return jsonify({"error": "Oops. Transaction not found"})
        
    except Exception as e:
        return jsonify({"Error": str(e)}), 500
    
    finally:
        cursor.close()
        connection.close()

    