# Controls graphql queries

import graphene
from graphql import GraphQLError
import psycopg2
from apis.v1.graphql.types import CashWalletType
import os
from dotenv import load_dotenv
load_dotenv()

class Query(graphene.ObjectType):
    cashwallet = graphene.Field(CashWalletType, user_id=graphene.Int(required=True))

    def resolve_cashwallet(self, info, cashwallet_id):
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
                "SELECT cashwallet_id, user_id, balance FROM cashwallets WHERE cashwallet_id = %s;",
                (cashwallet_id)
            )
            cashwallet = cursor.fetchone()
            cursor.close()
            connection.close()

            if not cashwallet:
                raise GraphQLError("User not found")
            
            return CashWalletType(
                cashwallet_id=cashwallet[0],
                user_id=cashwallet[1],
                balance=cashwallet[2]
            )
        except Exception as e:
            raise GraphQLError(f"Cannot get cashwallet: {str(e)}")