from flask import Blueprint, jsonify, request
from grpc_client.wallet_client import get_wallet_balance
from userService.models.user import User

app_views = Blueprint('app_views', __name__)

# Create a new user account
@app_views.route('/', methods=['POST'])
def register_user():
        data = request.get_json()
        user = User(
            data['first_name'],
            data['last_name'],
            data['email'],
            data['phone'],
            data['password']
        )
        try:
            user.create_user()
            return jsonify({"message": "Yaay. User acount successfully created!"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

# Get user wallet
#@app_views.route('/<int:user_id>/wallet', methods=['GET'])
#def get_user_wallet(user_id):
#    try:
#        wallet = get_wallet(user_id)
#        return jsonify({
#            "user_id": user_id,
#            "wallet_id": wallet_id
#        }), 200
#    except Exception as e:
#        return jsonify({"error": str(e)}), 500

# Get user by email
@app_views.route('/email/<email>', methods=['GET'], strict_slashes=False)
def get_user_by_email(email):
    try:
        user = User.find_user_by_email(email)
        if user:
            return jsonify({
                "first_name": user.first_name,
                "last_name": user.last_name,
                "user_id": user.user_id,
                "wallet_id": user.wallet_id
            }), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Get a user by the user_id
@app_views.route('/users/<int:user_id>', methods=["GET"], strict_slashes=False)
def get_user(user_id):
    try:
        user = User.find_user_by_id(user_id)
        if user:
            return jsonify({
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "wallet_id": user.wallet_id
            }), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": {e}}), 500