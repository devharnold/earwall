# graphql mutations

import graphene
from apis.v1.graphql.types import UserType
from graphene import String, Int, Field


class CreateUser(graphene.ObjectType):
    class Arguments:
        first_name = String(required=True)
        last_name = String(required=True)
        user_email = String(required=True)
        phone_number = Int(required=True)
        password = String(required=True)

    user = graphene.Field(lambda: UserType)

    def mutate(self, info, user_id, first_name, last_name, user_email, phone_number, password):
        new_user = {
            "user_id": user_id,
            "first_name": first_name,
            "last_name": last_name,
            "user_email": user_email,
            "phone_number": phone_number,
            "password": password
        }
        return CreateUser(new_user)
    
class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()