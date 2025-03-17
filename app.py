#!/usr/bin/env python3

from flask import Flask, jsonify
from linkpaypal import PaypalConfig
import os
from engine.db_storage import (
    get_db_connection,
    create_accounts_table,
    create_cashwallets_table,
    create_transactions_table,
    create_fraud_detection_table
)

app = Flask(__name__)

@app.route("/")
def create_tables():
    # Function to create db tables if they don't exist
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(create_accounts_table)
        cursor.execute(create_cashwallets_table)
        cursor.execute(create_transactions_table)
        cursor.execute(create_fraud_detection_table)

        connection.commit()
        print("All tables created successfully")
    except Exception as e:
        print(f"Error creating tables: Error!")
        connection.rollback()

@app.route("/")
def connect_paypal():
    pass

@app.route('/')
def home():
    # connect to the database
    connection = get_db_connection()
    cursor = connection.cursor

if __name__ == "__main__":
    create_tables()
    app.run(debug=True)