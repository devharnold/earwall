# graphql mutations

import graphene
from .types import AccountType, CashWalletType
from models.account import Account
from models.wallets.cashwallet import CashWallet
from engine.db_storage import get_db_connection
import random


class CreateAccount(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        initial_balance = graphene.Decimal(default_value=0.00) # Default value set to 0.00

    account = graphene.Field(AccountType)

    def mutate(self, info, user_id, initial_balance):
        conn = get_db_connection()
        cursor = conn.cursor()

        account_id = self.generate_account_id(cursor)
        account_number = self.generate_account_number(cursor)

        insert_query = """
            INSERT INTO accounts (account_id, account_number, user_id, balance, created_at)
            VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
            RETURNING account_id, account_number, user_id, balance;
        """
        cursor.execute(insert_query, (account_id, account_number, user_id, initial_balance))
        new_account = cursor.fetchone()
        
        conn.commit()
        cursor.close()
        conn.close()

        return CreateAccount(account=new_account)
    
    @staticmethod
    def generate_account_id(cursor):
        """Generate a unique 10-digit random account id"""
        while True:
            account_id = ''.join(str(random.randint(0, 9)) for _ in range(10))

            # check if the account id exists
            cursor.execute("SELECT account_id FROM accounts WHERE account_id = %s", (account_id,))
            existing_id = cursor.fetchone()

            if not existing_id:
                return account_id
            
    @staticmethod
    def generate_account_number(cursor):
        """Generate a unique 13-digit account_number"""
        while True:
            account_number = ''.join(str(random.randint(0, 9)) for _ in range(13))

            #check if the account number already exists
            cursor.execute("SELECT FROM accounts WHERE account_number = %s", (account_number,))
            existing_number = cursor.fetchone()

            if not existing_number:
                return account_number

# register the mutation
class Mutation(graphene.ObjectType):
    create_account = CreateAccount.Field()


class CreateCashWallet(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        initial_balance = graphene.Decimal(default_value=0.00)

    cashwallet = graphene.Field(CashWalletType)

    def mutate(self, info, user_id, initial_balance):
        conn = get_db_connection()
        cursor = conn.cursor()

        cashwallet_id = self.generate_cashwallet_id(cursor)

        insert_query = """
            INSERT INTO cashwallet (cashwallet_id, user_id, balance, created_at)
            VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
            RETURNING cashwallet_id, user_id, balance;
        """
        cursor.execute(insert_query, (cashwallet_id, user_id, initial_balance))
        new_cashwallet = cursor.fetchone()

        conn.commit()
        cursor.close()
        conn.close()

        return CreateCashWallet(cashwallet=new_cashwallet)
    
    @staticmethod
    def generate_cashwallet_id(cursor):
        """Generate a unique 10-digit random cashwallet_id"""
        while True:
            cashwallet_id = ''.join(str(random.randint(0, 9)) for _ in range(10))

            #check if the wallet_id exists
            cursor.execute("SELECT cashwallet_id FROM cashwallet WHERE cashwallet_id = %s", (cashwallet_id))
            existing_id = cursor.fetchone()

            if not existing_id:
                return cashwallet_id
            
class Mutation(graphene.ObjectType):
    create_cashwallet = CreateCashWallet.Field()