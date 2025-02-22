#!/usr/bin/env python3
from flask import Flask, jsonify
import os
from engine.db_storage import get_db_connection, create_audit_logs_table, create_cashwallet_table, create_fraud_detection_table, create_user_accounts_table, create_users_table, create_transactions_table

app = Flask(__name__)

@app.route("/")
def startApp():
    return (f"Hello World!")

def create_tables():
    """ Function to create db tables if they don't exist """
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(create_audit_logs_table)
        cursor.execute(create_cashwallet_table)
        cursor.execute(create_fraud_detection_table)
        cursor.execute(create_transactions_table)
        cursor.execute(create_users_table)
        cursor.execute(create_user_accounts_table)

        connection.commit()
        print("Tables created successfully!")

    except Exception as e:
        print(f"Error creating tables: {e}")
        connection.rollback()

    finally:
        cursor.close()
        connection.close()

@app.route('/')
def home():
    #connecting to our db
    connection = get_db_connection()
    cursor = connection.cursor()

    #execute a raw sql query
    cursor.execute('SELECT version();')

    db_version = cursor.fetchone()

    #close the connection
    cursor.close()
    connection.close()

    return jsonify({'PostgreSQL version': db_version[0]})

if __name__ == "__main__":
    create_tables()
    get_db_connection()
    app.run(debug=True)