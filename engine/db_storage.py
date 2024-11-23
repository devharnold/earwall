from flask import Flask
import os
import psycopg2
from dotenv import load_dotenv
import dotenv
from web3 import HTTPProvider


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
    - Business Account: One-to-Many with 'users'
    
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
        user_email VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        account_number  VARCHAR(14) UNIQUE,
        currency VARCHAR(50),
        balance NUMERIC DEFAULT 0,
        paypal_id VARCHAR(100) UNIQUE,
        paypal_email VARCHAR(100) UNIQUE,
        is_paypal_verified BOOLEAN DEFAULT FALSE, --verifies if paypal is linked and verified
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

    create_business_account_table_query = """
    CREATE TABLE IF NOT EXISTS business_account (
        id SERIAL PRIMARY KEY,
        business_name VARCHAR(100) NOT NULL,
        account_balance DECIMAL(20, 8) NOT NULL DEFAULT 0.00,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );"""
    try:
        cursor.execute(create_business_account_table_query)
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

    create_cashwallet_table_query = """
    CREATE TABLE IF NOT EXISTS cashwallets (
        cashwallet_id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES user(id) ON DELETE CASCADE,
        balance DECIMAL(20, 8) NOT NULL DEFAULT 0.00,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """
    try:
        cursor.execute(create_cashwallet_table_query)
        conn.commit()
    except Exception as e:
        print("Error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

with app.app_context():
    conn = get_db_connection()
    cursor = conn.cursor()

    create_accounts_table_query = """
    CREATE TABLE IF NOT EXISTS accounts (
        account_id VARCHAR(10) PRIMARY KEY CHECK (LENGTH(account_id) = 10 AND account_id ~ '^[0-9]+$'),
        account_number VARCHAR(13) UNIQUE CHECK (LENGTH(account_number) = 13 AND account_number ~ '^[0-9]+$'),
        user_id INTEGER REFERENCES user(id) ON DELETE CASCADE,
        account type VARCHAR(50) NOT NULL,
        balance DECIMAL(20, 8) NOT NULL DEFAULT 0.00,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """
    try:
        cursor.execute(create_accounts_table_query)
        conn.commit()
    except Exception as e:
        print("Error occured: {e}")
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
        wallet_id INTEGER REFERENCES cash_wallets(id) ON DELETE CASCADE,
        transaction type VARCHAR(50) NOT NULL,
        amount DECIMAL(20, 2) NOT NULL,
        status VARCHAR(20) DEFAULT 'pending',
        transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        source_account_id INT REFERENCES accounts(account_id) ON DELETE SET NULL,
        destination_account_id INT REFERENCES accounts(account)id ON DELETE SET NULL,
        source_cashwallet_id INT REFERENCES cashwallets(cashwallet_id) ON DELETE SET NULL,
        destination_cashwallet_id INT REFERENCES cashwallets(cashwallet_id) ON DELETE SET NULL,
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
        cryptowallet_id SERIAL PRIMARY KEY,
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