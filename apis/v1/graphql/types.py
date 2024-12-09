#graphql types
#!/usr/bin/env python3

import graphene

class UserType(object.ObjectType):
    id = graphene.Int()
    username = graphene.String()
    email = graphene.String()
    phone = graphene.Int()

class AccountType(object.ObjectType):
    id = graphene.Int()
    account_number = graphene.Int()
    user_id = graphene.Int()
    balance = graphene.Decimal()

class CashWalletType(object.ObjectType):
    cashwallet_id = graphene.Int()
    user_id = graphene.Int()
    account_id = graphene.Int()
    balance = graphene.Decimal()

class TransactionType(object.ObjectType):
    transaction_id = graphene.Int()
    user_id = graphene.Int()
    cashwallet_id = graphene.Int()
    amount = graphene.Float()
    balance = graphene.Float()