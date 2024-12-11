#graphql types
#!/usr/bin/env python3

import graphene

class UserType(graphene.ObjectType):
    id = graphene.Int()
    first_name = graphene.String()
    last_name = graphene.String()
    email = graphene.String()
    phone = graphene.Int()

class AccountType(graphene.ObjectType):
    id = graphene.Int()
    account_number = graphene.Int()
    user_id = graphene.Int()
    balance = graphene.Decimal()

class CashWalletType(graphene.ObjectType):
    cashwallet_id = graphene.Int()
    user_id = graphene.Int()
    account_id = graphene.Int()
    balance = graphene.Decimal()

class TransactionType(graphene.ObjectType):
    transaction_id = graphene.Int()
    user_id = graphene.Int()
    cashwallet_id = graphene.Int()
    amount = graphene.Float()
    balance = graphene.Float()