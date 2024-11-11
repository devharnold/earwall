# Controls graphql queries

import graphene
from .types import UserType, AccountType, CashWalletType
from models.user import User
from models.account import Account
from models.wallets.cashwallet import CashWallet

class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int(required=True))
    account = graphene.Field(AccountType, user_id=graphene.Int(required=True))
    cashwallet = graphene.Field(CashWalletType, user_id=graphene.Int(required=True))


    def resolve_user(self, info, id):
        return User.get_user_by_id(id)
    
    def resolve_account(self, info, user_id):
        return Account.get_account_by_user_id(user_id)
    
    def resolve_cashwallet(self, info, user_id):
        return CashWallet.get_cashwallet_by_user_id(user_id)