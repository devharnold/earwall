"""Objects that handle all default RESTFul API actions for users"""
from models.user import User
import os
from dotenv import load_dotenv
from engine.db_storage import get_db_connection
from apis.v1.views import app_views
import jwt
from flask import Flask, abort, jsonify, request, make_response
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET')


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_user():
    """Retrieves the list of all users or a specific user"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # retrieve query parameters
        user_id = request.args.get('user_id')

        if user_id:
            query = "SELECT id, first_name, last_name, email FROM users WHERE user_id = %s"
            cursor.execute(query, (user_id))
        else:
            query = "SELECT id, email FROM users"
            cursor.execute(query)

        users = cursor.fetchall()

        result = [
            {"id": row[0], "first_name": row[1], "last_name": row[2], "email": row[3]} for row in users
        ]
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        connection.close()

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def register_user():
    data = request.json()
    user = User(data['first_name'], data['last_name'], data['user_email'], data['password'])
    try:
        user.save()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def user_login():
    data = request.json

    if 'email' not in data or 'password' not in data:
        return jsonify({"error": "Email and password required"}), 400
    
    user = User.find_user_by_email(data['email'])
    if not user:
        return jsonify({"error": "Invalid email"}), 401
    
    if not user.verify_password(data['password']):
        return jsonify({"error": "Invalid password"}), 401
    
    token = jwt.encode(
        {"email": user.email},
        app.config['SECRET_KEY'],
        algorithm="HS256"
    )

    return jsonify({"message": "Login Successful"}), 200

@app_views.route('/users', methods=['PATCH'], strict_slashes=False)
def update_user_password():
    data = request.json

    if 'email' not in data or 'password' not in data:
        return jsonify({"error": "Email and password required"}), 400
    
    user = User.find_user_by_email(data['email'])
    if not user:
        return jsonify({"error": "Invalid email"}), 401
    
    if not user.verify_password(data['password']):
        return jsonify({"error": "Invalid password"})
    
    try:
        user = User.update_password()
        return jsonify({"message": "Password Updated"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500