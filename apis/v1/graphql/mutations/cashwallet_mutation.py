# graphql mutations

import graphene
from apis.v1.graphql.types import CashWalletType
from graphene import String, Int, Field
from engine.db_storage import get_db_connection
import random

class CreateCashWallet(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        initial_balance = graphene.Decimal(default_value=0.00)

    cashwallet = Field(lambda: CashWalletType)

    def mutate_cashwallet(self, info, user_id, initial_balance):
        conn = get_db_connection()
        cursor = conn.cursor()

        cashwallet_id = self.generate_cashwallet_id(cursor)

        insert_query = """
            INSERT INTO cashwallets (cashwallet_id, user_id, balance, created_at)
            VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
            RETURNING cashwallet_id, user_id, balance;
        """
        cursor.execute(insert_query, (cashwallet_id, user_id, initial_balance))
        new_cashwallet = cursor.fetchone()

        conn.commit()
        cursor.close()
        conn.close()

        return CreateCashWallet(cashwallet=new_cashwallet)
    
    @staticmethod
    def generate_cashwallet_id(cursor):
        """Generate a unique 10-digit random cashwallet_id"""
        while True:
            cashwallet_id = ''.join(str(random.randint(0, 9)) for _ in range(10))

            #check if the wallet_id exists
            cursor.execute("SELECT cashwallet_id FROM cashwallets WHERE cashwallet_id = %s", (cashwallet_id))
            existing_id = cursor.fetchone()

            if not existing_id:
                return cashwallet_id
            
class Mutation(graphene.ObjectType):
    create_cashwallet = CreateCashWallet.Field()