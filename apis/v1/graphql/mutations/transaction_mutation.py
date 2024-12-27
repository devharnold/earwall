import graphene
from apis.v1.graphql.types import TransactionType
from graphene import Field
from engine.db_storage import get_db_connection
import random

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
        cursor.execute(insert_query, (sender_user_email, receiver_user_email, sender_user_id, receiver_user_id, sender_cw_id))
        new_transaction = cursor.fetchone()

        connection.commit()
        cursor.close()
        connection.close()

        return CreateTransaction(transaction=new_transaction)
        
    @staticmethod
    def generate_transaction_id(cursor):
        """Generate a unique random 10-digit transaction id"""
        while True:
            transaction_id = ''.join(str(random.randint(0, 9))for _ in range(10))

            cursor.execute("SELECT transaction_id FROM transactions WHERE transaction_id = %s", (transaction_id))
            existing_id = cursor.fetchone()

            if not existing_id:
                return transaction_id
                

class Mutation(graphene.ObjectType):
    create_transaction = CreateTransaction.Field()