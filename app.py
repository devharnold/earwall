#!/usr/bin/env python3
from flask import Flask, jsonify
import os
import psycopg2
from dotenv import load_dotenv
from engine.db_storage import get_db_connection, create_audit_logs_table, create_cashwallet_table, create_fraud_detection_table, create_user_accounts_table, create_users_table, create_transactions_table

load_dotenv()
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_PASSWORD = os.getenv('DB_PASSWORD')

app = Flask(__name__)

@app.route("/")
def startApp():
    return (f"Hello World!")

@app.route('/')
def home():
    #connecting to our db
    connection = get_db_connection()
    cursor = connection.cursor()

    #execute a raw sql query
    cursor.execute('SELECT version();')
    cursor.execute(
        create_audit_logs_table,
        create_users_table,
        create_user_accounts_table,
        create_cashwallet_table,
        create_fraud_detection_table,
        create_transactions_table
    )

    db_version = cursor.fetchone()

    #close the connection
    cursor.close()
    connection.close()

    return jsonify({'PostgreSQL version': db_version})

if __name__ == "__main__":
    get_db_connection()
    app.run(debug=True)