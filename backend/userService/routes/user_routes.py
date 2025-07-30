from flask import Blueprint, jsonify, request
from backend.userService.grpc_client.wallet_client import get_wallet_balance
from backend.userService.models.user import User
from backend.utils.token import verify_token

app_views = Blueprint('app_views', __name__)

def get_user_from_token():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer'):
        return None, jsonify({"message": "No authorization header"}), 401
    token = auth_header.split("")[1]
    user_data = verify_token(token)
    if not user_data:
        return None, jsonify({"message": "Invalid token"}), 403
    return user_data, None, None


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

# Get user by email
@app_views.route('/email/<email>', methods=['GET'], strict_slashes=False)
def get_user_by_email(email):
    user_data, error_response, status_code = get_user_from_token()
    if error_response:
        return error_response, status_code

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
    user_data, error_response, status_code = get_user_from_token()
    if error_response:
        return error_response, status_code

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