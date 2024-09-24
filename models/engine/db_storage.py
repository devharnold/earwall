from flask import Flask
import os
import psycopg2
from dotenv import load_dotenv
import dotenv

app = Flask(__name__)

"""Initalizing the db and connection
"""

def get_db_connection():
    conn = psycopg2.connect(
        host = os.getenv('DB_HOST'),
        port = os.getenv('DB_PORT'),
        dbname = os.getenv('DB_NAME'),
        user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD')
    )
    return conn


"""
Summary of the tables relationships
    - User Accs: One-to-One with 'users'
    - Transactions: One-to-Many with 'users'
    - Crypto-Wallet: One-to-Many with 'users'
    - EFT methods: One-to-Many with 'users'
    - Audit trail: One-to-Many with 'users'
    
"""
with app.app_context():
    conn = get_db_connection()
    cursor = conn.cursor()

    #create the first table -> users table
    create_users_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    try:
        cursor.execute(create_users_table_query)
        conn.commit()
        print("Table created successfully")
    except Exception as e:
        print("Error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

with app.app_context():
    conn = get_db_connection()
    cursor = conn.cursor()

    create_transactions_table_query = """
    CREATE TABLE IF NOT EXISTS transactions (
        transaction_id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        transaction type VARCHAR(50) NOT NULL,
        amount DECIMAL(20, 2) NOT NULL,
        transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status VARCHAR(20) NOT NULL,
        description TEXT
    );
    """
    try:
        cursor.execute(create_transactions_table_query)
        conn.commit()
    except Exception as e:
        print("Error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

    
with app.app_context():
    conn = get_db_connection()
    cursor = conn.cursor()

    create_cryptowallets_table_query = """
    CREATE TABLE IF NOT EXISTS crypto-wallet (
        wallet_id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        cryptocurrency VARCHAR(50) NOT NULL,
        amount DECIMAL(20, 8) NOT NULL DEFAULT 0.00,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    try:
        cursor.execute(create_cryptowallets_table_query)
        conn.commit()
    except Exception as e:
        print("Error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

with app.app_context():
    conn = get_db_connection()
    cursor = conn.cursor()

    create_eftmethods_table_query = """
    CREATE TABLE IF NOT EXISTS eftmethods (
        method_id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        method_type VARCHAR(50) NOT NULL,
        account_number VARCHAR(100) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    try:
        cursor.execute(create_eftmethods_table_query)
        conn.commit()
    except Exception as e:
        print("Error occurred: {e}")
    finally:
        cursor.close()
        conn.close()
    
with app.app_context():
    conn = get_db_connection()
    cursor = conn.cursor()

    create_audittrail_table_query = """
    CREATE TABLE IF NOT EXISTS audittrail (
        audit_id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        action VARCHAR(100) NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        details TEXT
    );
    """
    try:
        cursor.execute(create_audittrail_table_query)
        conn.commit()
    except Exception as e:
        print("Error occurred: {e}")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run(debug=True)