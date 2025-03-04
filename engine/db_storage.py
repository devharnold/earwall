from flask import Flask
import os
import psycopg2
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

#def create_users_table():
#    """Create users table."""
#    connection = get_db_connection()
#    if connection:
#        try:
#            cursor = connection.cursor()
#            create_query = """
#                CREATE TABLE IF NOT EXISTS users (
#                    user_id SERIAL PRIMARY KEY,
#                    first_name VARCHAR(50) NOT NULL,
#                    last_name VARCHAR(50) NOT NULL,
#                    phone_number VARCHAR(15) UNIQUE NOT NULL,
#                    user_email VARCHAR(100) UNIQUE NOT NULL,
#                    password VARCHAR(255) NOT NULL,
#                    cashwallet_id VARCHAR(10) REFERENCES cashwallets(cwallet_id) ON DELETE CASCADE,
#                    account_number VARCHAR(14) UNIQUE,
#                    currency VARCHAR(50),
#                    balance NUMERIC DEFAULT 0,
#                    paypal_id VARCHAR(100) UNIQUE,
#                    paypal_email VARCHAR(100) UNIQUE,
#                    is_paypal_verified BOOLEAN DEFAULT FALSE,
#                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#                );
#            """
#            cursor.execute(create_query)
#            connection.commit()
#            print("Users table created successfully")
#        except Exception as e:
#            print(f"Error in creating users table: {e}")
#        finally:
#            cursor.close()
#            connection.close()

def create_accounts_table():
    """Create accounts table."""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            create_query = """
                CREATE TABLE IF NOT EXISTS accounts (
                    account_id SERIAL PRIMARY KEY,
                    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
                    user_email VARCHAR(100) REFERENCES users(user_email) ON DELETE CASCADE,
                    phone_number VARCHAR(15) REFERENCES users(phone_number) UNIQUE NOT NULL,
                    balance DECIMAL(20, 8) NOT NULL DEFAULT 0.00,
                    currency VARCHAR(3) DEFAULT 'USD',
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
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

def create_cashwallets_table():
    """Create cashwallets table."""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            create_query = """
                CREATE TABLE IF NOT EXISTS cashwallets (
                    cwallet_id VARCHAR(10) PRIMARY KEY,
                    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
                    account_type VARCHAR(50) NOT NULL,
                    balance DECIMAL(20, 8) NOT NULL DEFAULT 0.00,
                    currency VARCHAR(10) NOT NULL,
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

def create_business_account_table():
    """Create business_accounts table."""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            create_query = """
                CREATE TABLE IF NOT EXISTS business_accounts (
                    bizacc_id SERIAL PRIMARY KEY,
                    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
                    business_name VARCHAR(100) UNIQUE NOT NULL,
                    account_balance DECIMAL(20, 8) NOT NULL DEFAULT 0.00,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
            cursor.execute(create_query)
            connection.commit()
            print("Business accounts table created successfully")
        except Exception as e:
            print(f"Error in creating business accounts table: {e}")
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
                    transaction_id SERIAL PRIMARY KEY NOT NULL,
                    sender_user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
                    receiver_user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
                    from_currency VARCHAR(3) NOT NULL,
                    to_currency VARCHAR(3) NOT NULL,
                    transaction_type VARCHAR(50) NOT NULL,
                    amount DECIMAL(20, 2) NOT NULL,
                    source_cwallet_id VARCHAR(10) REFERENCES cashwallets(cwallet_id) ON DELETE SET NULL,
                    destination_cwallet_id VARCHAR(10) REFERENCES cashwallets(cwallet_id) ON DELETE SET NULL,
                    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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

def create_fraud_detection_table():
    """Create fraud detection table."""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            create_query = """
                CREATE TABLE IF NOT EXISTS fraud_detection (
                    activity_id VARCHAR(8) PRIMARY KEY,
                    transaction_id INT REFERENCES transactions(transaction_id) ON DELETE CASCADE,
                    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
                    reason VARCHAR(20) NOT NULL
                );
            """
            cursor.execute(create_query)
            connection.commit()
            print("Fraud detection table created successfully")
        except Exception as e:
            print(f"Error in creating fraud detection table: {e}")
        finally:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    #create_users_table()
    create_cashwallets_table()
    create_business_account_table()
    create_accounts_table()
    create_transactions_table()
    create_fraud_detection_table()
    print("All tables created successfully")
    app.run(debug=True)
