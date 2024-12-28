# Controls graphql queries

import graphene
from graphql import GraphQLError
from apis.v1.graphql.types import CashWalletType
from engine.db_storage import get_db_connection
import os
from dotenv import load_dotenv
load_dotenv()

class Query(graphene.ObjectType):
    cashwallet = graphene.Field(CashWalletType, user_id=graphene.Int(required=True))

    def resolve_cashwallet(self, info, cashwallet_id):
        try:
            connection = get_db_connection()
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