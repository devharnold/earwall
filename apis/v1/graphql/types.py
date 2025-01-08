#graphql types
#!/usr/bin/env python3

import graphene

class UserType(graphene.ObjectType):
    user_id = graphene.Int()
    first_name = graphene.String()
    last_name = graphene.String()
    email = graphene.String()
    phone = graphene.Int()

class AccountType(graphene.ObjectType):
    account_id = graphene.Int()
    account_number = graphene.Int()
    user_id = graphene.Int()
    balance = graphene.Float()

class CashWalletType(graphene.ObjectType):
    cashwallet_id = graphene.Int()
    user_id = graphene.Int()
    account_id = graphene.Int()
    balance = graphene.Float()

class TransactionType(graphene.ObjectType):
    transaction_id = graphene.Int()
    sender_user_id = graphene.Int()
    receiver_user_id = graphene.Int()
    from_currency = graphene.String()
    to_currency = graphene.String()
    amount = graphene.Float()

class BatchTransactionType(graphene.ObjectType):
    b_transaction_id = graphene.String()
    sender_user_id = graphene.Int()
    receiver_user_id = graphene.Int()
    from_currency = graphene.String()
    to_currency = graphene.String()
    amount = graphene.Float()