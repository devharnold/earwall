# Controls graphql queries

import graphene
from .types import UserType, AccountType, CashWalletType
from flask import jsonify
from models.user import User
from models.account import Account
from engine.db_storage import get_db_connection
from models.wallets.cashwallet import CashWallet

class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int(required=True))
    account = graphene.Field(AccountType, user_id=graphene.Int(required=True))
    cashwallet = graphene.Field(CashWalletType, user_id=graphene.Int(required=True))

    def resolve_user(self, info, user_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id, name, email FROM users;")
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

            cursor.execute("SELECT wallet_id, user_id, balance FROM cashwallet;")
            cashwallets = cursor.fetchall()
            cursor.close()
            conn.close()
        except Exception as e:
            return jsonify({"Error": "Cannot get wallets"})
        return [CashWalletType(cashwallet_id=row[0], user_id=row[1], balance=row[2]) for row in cashwallets]
    
    #
    #def resolve_account(self, info, user_id):
    #    return Account.get_account_by_user_id(user_id)
    #
    #def resolve_cashwallet(self, info, user_id):
    #    return CashWallet.get_cashwallet_by_user_id(user_id)