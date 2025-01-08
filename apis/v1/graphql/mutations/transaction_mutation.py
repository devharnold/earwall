import graphene
from apis.v1.graphql.types import TransactionType
from graphene import Field
from engine.db_storage import get_db_connection
import random

class CreateTransaction(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        user_email = graphene.String(required=True)
        from_currency = graphene.String(required=True)
        to_currency = graphene.String(required=True)
        amount = graphene.Decimal(required=True)

        transaction = Field(lambda: TransactionType)

    def mutate_transaction(self, info, user_id, user_email, from_currency, to_currency, amount):
        connection = get_db_connection()
        cursor = connection.cursor()

        transaction_id = self.generate_transaction_id(cursor)

        insert_query = """
            INSERT INTO transactions (user_id, user_email, from_currency, to_currency, amount)
            VALUES (%s, %s, %s, %s, %s, CURRENT TIMESTAMP)
            RETURNING user_id, user_email, from_currency, to_currency, amount
        """
        cursor.execute(insert_query, (user_id, user_email, from_currency, to_currency, amount))
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