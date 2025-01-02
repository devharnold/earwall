"""Batch transaction mutation class"""
import graphene
from apis.v1.graphql.types import BatchTransactionType
from graphene import Field
from engine.db_storage import get_db_connection
import random
import string

class CreateBatchTransaction(graphene.Mutation):
    class Arguments:
        sender_user_id = graphene.String(required=True)
        receiver_user_id = graphene.String(required=True)
        from_currency = graphene.String(required=True)
        to_currency = graphene.String(required=True)
        amount = graphene.Decimal(required=True)

        batch_trnasaction = Field(lambda: BatchTransactionType)

        def mutate_batch_transaction(self, info, sender_user_id, receiver_user_id, from_currency, to_currency, amount):
            connection = get_db_connection()
            cursor = connection.cursor()
            connection.autocommit = False

            batch_transaction_id = self.generate_b_transaction_id(cursor)

            insert_query = """
                INSERT INTO batch_transactions (sender_user_id, receiver_user_id, from_currency, to_currency, amount)
                """
            cursor.execute(insert_query, (sender_user_id, receiver_user_id, from_currency, to_currency))
            new_batch_transaction = cursor.fetchone()

            connection.commit()
            cursor.close()
            connection.close()

            return CreateBatchTransaction(batch_transaction=new_batch_transaction)
        
        @staticmethod
        def generate_b_transaction_id(cursor, length=9):
            """Generate a random 10-digit varchar batch transaction id"""
            while True:
                characters = string.ascii_letters + string.digits
                b_transaction_id =  ''.join(random.choices(characters, k=length))

                cursor.execute("SELECT b_transaction_id FROM batch_transactions WHERE b_transaction_id = %s", (b_transaction_id))
                existing_id = cursor.fetchone()

                if not existing_id:
                    return b_transaction_id
                
class Mutation(graphene.ObjectType):
    create_batch_transaction = CreateBatchTransaction.Field()
            
