#Objects that handle all default RESTFul API actions for users
from backend.models.user import User
import os
from dotenv import load_dotenv
from backend.engine.db_storage import get_db_connection
from backend.apis.v1.views import app_views
import jwt
from cryptography.hazmat.primitives import serialization
from flask import Flask, abort, jsonify, request, make_response
load_dotenv()

private_key = os.getenv("KEY_FINGERPRINT")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET')

#Retrieves the list of all users
@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_user():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # retrieve query parameters
        user_id = request.args.get('user_id', 'user_email')

        if user_id:
            query = "SELECT * FROM users"
            cursor.execute(query)
        else:
            query = "SELECT user_id, user_email FROM users"
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

# Get a user by the user_id
@app_views.route('/users/<int:user_id>', methods=["GET"], strict_slashes=False)
def get_user():
    data = request.json
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # retrieve query params
        user_id = request.args.get('user_id')
        
        query = "SELECT * FROM users WHERE user_id = %s"
        cursor.execute(query)
        
        user = cursor.fetchone()

        result = [
            {"id": row[0], "first_name": row[1], "last_name": row[2], "user_email": row[3]} for row in user
        ]
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        connection.close()
        cursor.close()
    
#Route to update the users password
@app_views.route('/users/<int:user_id>', methods=['PATCH'], strict_slashes=False)
def update_user_password():
    data = request.json

    if 'email' not in data or 'password' not in data:
        return jsonify({"error": "Email and password required"}), 400
    
    user = User.find_user_by_email(data['email'])
    if not user:
        return jsonify({"error": "Invalid email"}), 401
    
    if not user.verify_password(data['password']):
        return jsonify({"error": "Invalid password"})

    token = jwt.encode (
        {"email": user.email},
        app.config['SECRET_KEY'],
        algorithm='HS256'
    )
    
    try:
        user = User.update_password()
        return jsonify({"message": "Password Updated"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

#@app_views.route('/users', methods=['POST'], strict_slashes=False)
#def register_user():
#    data = request.json()
#    user = User(data['first_name'], data['last_name'], data['user_email'], data['password'])
#    try:
#        user.save()
#        return jsonify({"message": "User registered successfully"}), 201
#    except Exception as e:
#        return jsonify({"error": str(e)}), 500
#    
#
#@app_views.route('/users', methods=['POST'], strict_slashes=False)
#def user_login():
#    data = request.json
#
#    if 'email' not in data or 'password' not in data:
#        return jsonify({"error": "Email and password required"}), 400
#    
#    user = User.find_user_by_email(data['email'])
#    if not user:
#        return jsonify({"error": "Invalid email"}), 401
#    
#    if not user.verify_password(data['password']):
#        return jsonify({"error": "Invalid password"}), 401
#    
#    token = jwt.encode(
#        {"email": user.email},
#        app.config['SECRET_KEY'],
#        algorithm="HS256"
#    )
#
#    return jsonify({"message": "Login Successful"}), 200