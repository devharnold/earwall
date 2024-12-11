import graphene
from apis.v1.graphql.types import TransactionType
from graphene import Field
from engine.db_storage import get_db_connection

class CreateTransaction(graphene.Mutation):
    class Arguments:
        sender_user_email = graphene.String(required=True)
        receiver_user_email = graphene.String(required=True)
        sender_user_id = graphene.String(required=True)
        receiver_user_id = graphene.String(required=True)
        sender_cw_id = graphene.String(required=True)
        receiver_cw_id = graphene.String(required=True)
        sender_currency = graphene.String(required=True)
        receiver_currency = graphene.String(required=True)
        amount = graphene.String(required=True)

        transaction = Field(lambda: TransactionType)

        def mutate_transaction(self, info, sender_user_email, receiver_user_email, sender_user_id, receiver_user_id, sender_cw_id, receiver_cw_id, sender_currency, receiver_currency, amount):
            connection = get_db_connection()
            cursor = connection.cursor()

            transaction_id = self.generate_transaction_id(cursor)

            insert_query = """
                INSERT INTO transactions (sender_user_email, receiver_user_email, sender_user_id, receiver_user_id, sender_cw_id)"""