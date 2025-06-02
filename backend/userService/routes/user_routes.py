from flask import Blueprint, jsonify, request
from grpc_client.wallet_client import get_wallet_balance

app_views = Blueprint('app_views', __name__)

@app_views.route('/users/<int:user_id>/wallet', methods=['GET'])
def get_user_wallet(user_id):
    try:
        balance = get_wallet_balance(user_id)
        return jsonify({
            "user_id": user_id,
            "balance": balance
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app_views.route('/users/<int:user_id>/email', methods=['GET'], strict_slashes=False)
def get_user_by_email(user_email)
    try:
        