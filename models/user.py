#!/usr/bin/env python3

"""Holds the user model class"""

import models
import hashlib
import psycopg2
import os
from os import getenv
from models import BaseModel
from engine.db_storage import get_db_connection
from web3 import HTTPProvider


class User(BaseModel):
    """Representation of a user model"""
    def __init__(self, first_name, last_name, user_email, password=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = user_email
        self.password = password

    @staticmethod
    def hash_password(password):
        """Hash a user's password using the sha256 algorithm and add salt"""
        salt = os.urandom(16) # New salt
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return salt, hashed_password
    
    def save(self):
        """Saves a new user to the db"""
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO users (first_name, last_name, user_email, password)
        VALUES (%s, %s, %s, %s);
        """
        try:
            cursor.execute(query, (self.first_name, self.last_name, self.user_email, self.password))
            conn.commit()
            print("User saved successfully")
        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_password(user_email, new_password):
        """Updates the password of an existing user."""
        conn = get_db_connection()
        cursor = conn.cursor()

        hashed_password = hashlib.sha256(new_password.encode()).hexdigest()

        query = "UPDATE users SET password = %s WHERE email = %s;"
        try:
            cursor.execute(query, (hashed_password, user_email))
            conn.commit()
            print("Password saved successfully")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()