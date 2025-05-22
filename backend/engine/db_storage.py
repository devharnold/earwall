from flask import Flask
import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

class DatabaseManager:
    def __init__(self):
        self.connection = self.get_db_connection()

    def get_db_connection(self):
        # Establish DB connection
        try:
            return psycopg2.connect(
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
            )
        except Exception as e:
            print(f"Failed to connect to DB: {e}")
            return None
        
    
    def create_users_table(self):
        # Create users table
        if self.connection:
            try:
                cursor = self.connection.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        user_id SERIAL PRIMARY KEY,
                        first_name VARCHAR(50) NOT NULL,
                        last_name VARCHAR(50) NOT NULL,
                        phone_number VARCHAR(15) UNIQUE NOT NULL,
                        user_email VARCHAR(100) UNIQUE NOT NULL,
                        password VARCHAR(255) NOT NULL,
                        wallet_id VARCHAR(10) REFERENCES wallets(wallet_id) ON DELETE CASCADE,
                        currency VARCHAR(50),
                        balance NUMERIC DEFAULT 0,
                        paypal_id VARCHAR(100) UNIQUE,
                        paypal_email VARCHAR(100) UNIQUE,
                        is_paypal_verified BOOLEAN DEFAULT FALSE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                self.connection.commit()
                print("Users table created successfully")
            except Exception as e:
                print(f"Error in creating users table: {e}")
            finally:
                cursor.close()

    def create_wallets_table(self):
        # Create wallets table
        if self.connection:
            try:
                cursor = self.connection.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS wallets (
                        wallet_id VARCHAR(10) PRIMARY KEY,
                        user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
                        account_type VARCHAR(50) NOT NULL,
                        balance DECIMAL(20, 8) NOT NULL DEFAULT 0.00,
                        currency VARCHAR(10) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                self.connection.commit()
                print("Wallets table created successfully")
            except Exception as e:
                print(f"Error in creating wallets table: {e}")
            finally:
                cursor.close()

    def create_transactions_table(self):
        # Create transactions table
        if self.connection:
            try:
                cursor = self.connection.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS transactions (
                        transaction_id SERIAL PRIMARY KEY NOT NULL,
                        sender_user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
                        receiver_user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
                        from_currency VARCHAR(3) NOT NULL,
                        to_currency VARCHAR(3) NOT NULL,
                        transaction_type VARCHAR(30) DEFAULT 'P2P-Transfer' NOT NULL CHECK (transaction_type IN ('P2P', 'Wallet deposit', 'Wallet withdrawal')),
                        amount DECIMAL(20, 2) NOT NULL,
                        source_cwallet_id VARCHAR(10) REFERENCES cashwallets(cwallet_id) ON DELETE SET NULL,
                        destination_cwallet_id VARCHAR(10) REFERENCES cashwallets(cwallet_id) ON DELETE SET NULL,
                        transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        description TEXT
                    );
                """)
                self.connection.commit()
                print("Transactions table created successfully")
            except Exception as e:
                print(f"Error in creating transactions table: {e}")
            finally:
                cursor.close()

    def close_connection(self):
        # Close the DB connection
        if self.connection:
            self.connection.close()


if __name__ == "__main__":
    db_manager = DatabaseManager()
    db_manager.create_users_table()
    db_manager.create_wallets_table()
    db_manager.create_transactions_table()
    db_manager.close_connection()
    print("All tables created successfully")
    app.run(debug=True)
