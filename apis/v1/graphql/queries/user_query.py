# Controls graphql queries

import graphene
from graphql import GraphQLError
import psycopg2
from apis.v1.graphql.types import UserType
import os
from dotenv import load_dotenv
load_dotenv()

class Query(graphene.ObjectType):
    user = graphene.Field(UserType, user_id=graphene.Int(required=True))

    def resolve_user(self, info, user_id):
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
                "SELECT user_id, first_name, last_name, user_email FROM users WHERE user_id = %s;",
                (user_id)
            )
            user = cursor.fetchone()
            cursor.close()
            connection.close()

            if not user:
                raise GraphQLError("User not found")
            
            return UserType(
                user_id=user[0],
                first_name=user[1],
                last_name=user[2],
                user_email=user[3]
            )
        except Exception as e:
            raise GraphQLError(f"Cannot get users: {str(e)}")