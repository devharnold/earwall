# graphql mutations

import graphene
from apis.v1.graphql.types import UserType
from graphene import String, Int, Field
from engine.db_storage import get_db_connection
import random


class CreateUser(graphene.ObjectType):
    class Arguments:
        first_name = String(required=True)
        last_name = String(required=True)
        user_email = String(required=True)
        phone_number = Int(required=True)
        password = String(required=True)

    user = graphene.Field(lambda: UserType)

    def mutate_user(self, info, first_name, last_name, user_email, phone_number, password):
        connection = get_db_connection()
        cursor = connection.cursor()

        user_id = self.generate_user_id(cursor)

        insert_query = """
            INSERT INTO users (user_id, first_name, last_name, user_email, phone_number, password)
            VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            RETURNING user_id, first_name, last_name, user_email, phone_number, password;
            """
        cursor.execute(insert_query, (user_id, first_name, last_name, user_email, phone_number, password))
        new_user = cursor.fetchone()

        connection.commit()
        cursor.close()
        connection.close()


        return CreateUser(new_user=CreateUser)
    
    @staticmethod
    def generate_user_id(cursor):
        """Generate a random unique 10-digit user_id"""
        while True:
            user_id = ''.join(str(random.randint(0, 9))for _ in range(10))

            # check if the user_id already exists in the database
            cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id))
            existing_id = cursor.fetchone()

            if not existing_id:
                return user_id
            
class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
