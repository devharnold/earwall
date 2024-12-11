# Controls transaction graphql queries

import graphene
from graphql import GraphQLError
import psycopg2
from apis.v1.graphql.types import TransactionType
import os
from dotenv import load_dotenv
load_dotenv()

class Query(graphene.ObjectType):
    transaction = graphene.Field(TransactionType, cashwallet_id=graphene.Int(required=True))

    def resolve_user(self, info, transaction_id):
        try:
            connection = psycopg2.connect(
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT'),
                dbname=os.getnev('DB_NAME'),
                user=os.getenv('DB_NAME'),
                password=os.getenv('DB_PASSWORD')
            )
            cursor = connection.cursor()

            cursor.execute(
                "SELECT stransaction_id, ender_user_email, receiver_user_email, sender_user_id, receiver_user_id, sender_cw_id, receiver_cw_id, sender_currency, receiver_currency, amount FROM transactions WHERE transaction_id = %s;",
                (transaction_id)
            )
            transaction = cursor.fetchone()
            cursor.close()
            connection.close()

            if not transaction:
                raise GraphQLError("Cannot trace Transaction not found")
            
            return TransactionType(
                transaction_id=transaction[0],
                sender_user_email=transaction[1],
                receiver_user_email=transaction[2],
                sender_user_id=transaction[3],
                receiver_transaction_id=transaction[4],
                sender_cw_id=transaction[5],
                receiver_cw_id=transaction[6],
                sender_currency=transaction[7],
                receiver_currency=transaction[8],
                amount=transaction[9]
            )
        except Exception as e:
            raise GraphQLError(f"Cannot get users: {str(e)}")