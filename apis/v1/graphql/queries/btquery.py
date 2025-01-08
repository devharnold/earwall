#Controls graphql queries

import graphene
from graphql import GraphQLError
from engine.db_storage import get_db_connection
from apis.v1.graphql.types import BatchTransactionType

class BatchQuery(graphene.ObjectType):
    batch_transaction = graphene.Field(BatchTransactionType)

    def resolve_b_transaction(self, info, b_transaction_id):
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            cursor.execute(
                "SELECT b_transaction_id, sender_user_id, receiver_user_id, from_currency, to_currency, amount FROM batch_transactions WHERE b_transaction_id = %s"
                (b_transaction_id)
            )
            batch_transaction = cursor.fetchone()
            cursor.close()
            connection.close()

            if not batch_transaction:
                raise GraphQLError("Cannot Transactions not found")

            return BatchTransactionType(
                b_transaction_id=batch_transaction[0],
                sender_user_id=batch_transaction[1],
                receiver_user_id=batch_transaction[2],
                from_currency=batch_transaction[3],
                to_currency=batch_transaction[4],
                amount=batch_transaction[5]
            )
        except Exception as e:
            raise GraphQLError(f"Cannot get transactions: {str(e)}")