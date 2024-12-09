# Controls graphql queries

import graphene
from .types import UserType, AccountType, CashWalletType, TransactionType
from flask import jsonify
from engine.db_storage import get_db_connection

class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int(required=True))
    account = graphene.Field(AccountType, user_id=graphene.Int(required=True))
    cashwallet = graphene.Field(CashWalletType, user_id=graphene.Int(required=True))

    def resolve_user(self, info, user_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT user_id, first_name, last_name, user_email FROM users;")
            users = cursor.fetchall()
            cursor.close()
            conn.close()
        except Exception as e:
            return jsonify({"error": "Cannot get users"})
        return [UserType(user_id=row[0], name=row[1], email=row[2]) for row in users]
    
    def resolve_acccount(self, info, user_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT account_id, account_number, user_id, balance FROM accounts;")
            accounts = cursor.fetchall()
            cursor.close()
            conn.close()
        except Exception as e:
            return jsonify({"error": "Cannot get accounts"})
        return [AccountType(account_id=row[0], account_number=row[1], user_id=row[2], balance=row[3]) for row in accounts]
    
    def resolve_cashwallet(self, info, user_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT cashwallet_id, user_id, balance FROM cashwallet;")
            cashwallets = cursor.fetchall()
            cursor.close()
            conn.close()
        except Exception as e:
            return jsonify({"Error": "Cannot get wallets"})
        return [CashWalletType(cashwallet_id=row[0], user_id=row[1], balance=row[2]) for row in cashwallets]
    
    def resolve_transaction(self, transaction_id):
        try:
            conn=get_db_connection()
            cursor=conn.cursor()

            cursor.execute("SELECT transaction_id, sender_user_id, receiver_user_id, sender_cw_id, receiver_cw_id, amount FROM transactions;")
            transactions = cursor.fetchall()
            cursor.close()
            conn.close()
        except Exception as e:
            return jsonify({"Error": "Cannot get transactions"})
        return [TransactionType(transaction_id=row[0], user_id=row[1], amount=row[2]) for row in transactions]