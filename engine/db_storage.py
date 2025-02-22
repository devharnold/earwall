from flask import Flask
import os
import psycopg2
import dotenv
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)


def get_db_connection():
    """Establish DB connection."""
    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )
        return connection
    except Exception as e:
        print(f"Failed to connect to DB: {e}")
        return None


def create_users_table():
    """Create users table."""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            create_query = """
                CREATE TABLE IF NOT EXISTS users (
                    user_id SERIAL PRIMARY KEY,
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50) NOT NULL,
                    user_email VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    cashwallet_id REFERENCES cashwallets(id) ON DELETE CASCADE,
                    account_number VARCHAR(14) UNIQUE,
                    currency VARCHAR(50),
                    balance NUMERIC DEFAULT 0,
                    paypal_id VARCHAR(100) UNIQUE,
                    paypal_email VARCHAR(100) UNIQUE,
                    is_paypal_verified BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
            cursor.execute(create_query)
            connection.commit()
            print("Users table created successfully")
        except Exception as e:
            print(f"Error in creating users table: {e}")
        finally:
            cursor.close()
            connection.close()


def create_business_account_table():
    """Create business_account table."""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            create_query = """
                CREATE TABLE IF NOT EXISTS business_account (
                    bizacc_id SERIAL PRIMARY KEY,
                    business_name VARCHAR(100) NOT NULL,
                    account_balance DECIMAL(20, 8) NOT NULL DEFAULT 0.00,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
            cursor.execute(create_query)
            connection.commit()
            print("Business account table created successfully")
        except Exception as e:
            print(f"Error in creating business account table: {e}")
        finally:
            cursor.close()
            connection.close()


def create_cashwallet_table():
    """Create cashwallet table."""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            create_query = """
                CREATE TABLE IF NOT EXISTS cashwallets (
                    cw_id SERIAL PRIMARY KEY,
                    user_id REFERENCES users(id) ON DELETE CASCADE,
                    user_email STRING REFERENCES users(user_email) ON DELETE CASCADE,
                    balance DECIMAL(20, 8) NOT NULL DEFAULT 0.00,
                    currency VARCHAR(3) DEFAULT 'USD',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
            cursor.execute(create_query)
            connection.commit()
            print("Cashwallets table created successfully")
        except Exception as e:
            print(f"Error in creating cashwallets table: {e}")
        finally:
            cursor.close()
            connection.close()


def create_transactions_table():
    """Create transactions table."""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            create_query = """
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id SERIAL PRIMARY KEY,
                    sender_user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    receiver_user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    from_currency VARCHAR(3) NOT NULL,
                    to_currency VARCHAR(3) NOT NULL,
                    transaction_type VARCHAR(50) NOT NULL,
                    amount DECIMAL(20, 2) NOT NULL,
                    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    source_account_id VARCHAR(10) REFERENCES accounts(account_id) ON DELETE SET NULL,
                    destination_account_id VARCHAR(10) REFERENCES accounts(account_id) ON DELETE SET NULL,
                    description TEXT
                );
            """
            cursor.execute(create_query)
            connection.commit()
            print("Transactions table created successfully")
        except Exception as e:
            print(f"Error in creating transactions table: {e}")
        finally:
            cursor.close()
            connection.close()


def create_user_accounts_table():
    """Create accounts table."""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            create_query = """
                CREATE TABLE IF NOT EXISTS user_accounts (
                    account_id VARCHAR(10) PRIMARY KEY,
                    account_number VARCHAR(13) UNIQUE,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    account_type VARCHAR(50) NOT NULL,
                    balance DECIMAL(20, 8) NOT NULL DEFAULT 0.00,
                    currency VARCHAR(10) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
            cursor.execute(create_query)
            connection.commit()
            print("Accounts table created successfully")
        except Exception as e:
            print(f"Error in creating accounts table: {e}")
        finally:
            cursor.close()
            connection.close()

def create_audit_logs_table():
    """Create audit logs table"""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            create_query = """
                CREATE TABLE IF NOT EXISTS audit_logs (
                    log_id VARCHAR(10) PRIMARY KEY,
                    action_type VARCHAR(100) NOT NULL,
                    user_id REFERENCES users(user_id),
                    details,
                    ip_address 
                )
            """
            cursor.execute(create_query)
            connection.commit()
            print("Accounts table created successfully")
        except Exception as e:
            print(f"Error creating accounts table: {e}")
        finally:
            cursor.close()
            connection.close()

def create_fraud_detection_table():
    """Table that lists activites in fraud detection"""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            create_query = """
                CREATE TABLE IF NOT EXISTS fraud_detection (
                    activity_id VARCHAR(8) PRIMARY KEY,
                    transaction_id REFERENCES transactions(transaction_id),
                    user_id REFERENCES users(user_id),
                    reason VARCHAR(20)NOT NULL
                )
            """
            cursor.execute(create_query)
            connection.commit()
            print("Accounts table created successfully")
        except Exception as e:
            print(f"Error creating accounts table: {e}")
        finally:
            cursor.close()
            connection.close()


if __name__ == "__main__":
    create_users_table()
    create_business_account_table()
    create_cashwallet_table()
    create_transactions_table()
    create_user_accounts_table()
    create_audit_logs_table()
    create_fraud_detection_table()
    print("All tables created successfully")
    app.run(debug=True)