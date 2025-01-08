# Controls transaction graphql queries

import graphene
from graphql import GraphQLError
from engine.db_storage import get_db_connection
from apis.v1.graphql.types import TransactionType
import os
from dotenv import load_dotenv
load_dotenv()

class Query(graphene.ObjectType):
    transaction = graphene.Field(TransactionType, cashwallet_id=graphene.Int(required=True))

    def resolve_user(self, info, transaction_id):
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            cursor.execute(
                "SELECT transaction_id, user_id, user_email, from_currency, to_currency, amount FROM transactions WHERE transaction_id = %s;",
                (transaction_id)
            )
            transaction = cursor.fetchone()
            cursor.close()
            connection.close()

            if not transaction:
                raise GraphQLError("Cannot trace Transaction not found")
            
            return TransactionType(
                user_id=transaction[0],
                user_email=transaction[1],
                from_currency=transaction[2],
                to_currency=transaction[3],
                amount=transaction[4],
                transaction_id=transaction[5]
            )
        except Exception as e:
            raise GraphQLError(f"Cannot get transaction: {str(e)}")