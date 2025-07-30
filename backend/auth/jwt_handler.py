import jwt
import os
import dotenv
from functools import wraps
from dotenv import load_dotenv
from flask import request, HTTPException, jsonify
from jwt import ExpiredSignatureError, InvalidTokenError

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def get_current_user():
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer"):
        return jsonify({"detail": "No token provided"}), 401

    try:
        payload = jwt.decode(token[:7], SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        return jsonify({"detail": "Token has expired"}), 401
    except InvalidTokenError:
        return jsonify({"detail": "Invalid Token"}), 403

def require_role(self):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            result = get_current_user()
            if isinstance(result, tuple):
                return result
            user = result
            if user.get("role") != role:
                return jsonify({"detail": "Not Authorized"}), 401
            return f(user, *args, **kwargs)
        return decorated_function
    return decorator()