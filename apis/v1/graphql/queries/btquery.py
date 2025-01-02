#Controls graphql queries

import graphene
from graphql import GraphQLError
from engine.db_storage import get_db_connection
from apis.v1.graphql.types import BatchTransactionType

class BatchQuery(graphene.ObjectType):
    batch_transaction = graphene.Field(BatchTransactionType)

    def resolve_b_transaction(self, info, b_transaction_id):
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT b_transaction_id, sender_user_id, receiver_user_id, from_currency, to_currency, amount FROM batch_transactions WHERE b_transaction_id = %s"
            (b_transaction_id)
        )