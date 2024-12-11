import pytest
from graphene.test import Client
from graphene import Schema, ObjectType
from apis.v1.graphql.schema import Mutation
from apis.v1.graphql.queries import Query
from unittest.mock import MagicMock

@pytest.fixture
def mocked_db_connection():
    """Mock the database connection"""
    mock_conn = MagicMock()
    mock_cursor = mock_conn.cursor.return_value
    yield mock_conn, mock_cursor


@pytest.fixture
def client():
    """Graphene test client for executing mutations"""
    schema = Schema(query=Query, mutation=Mutation)
    from graphene.test import Client
    return Client(schema=schema)

class TestUserMutation:
    """Tests for the GraphQL user mutation"""
    def test_user_mutation(self, client, mocked_db_connection):
        mock_conn, mock_cursor = mocked_db_connection  # Unpack the tuple returned by the fixture
        mock_cursor.fetchone.return_value = {
            "user_id": "12345678",
            "first_name": "John",
            "last_name": "Doe",
            "user_email": "john.doe@example.com",
            "phone_number": 712345678,
            "password": "securepassword"
        }

        mutation = """
        mutation CreateUser($firstName: String!, $lastName: String!, $userEmail: String!, $phoneNumber: Int!, $password: String!) {
            createUser(firstName: $firstName, lastName: $lastName, userEmail: $userEmail, phoneNumber: $phoneNumber, password: $password) {
                user {
                    user_id
                    first_name
                    last_name
                    email
                    phone_number
                }
            }
        }
        """
        variables = {
            "firstName": "John",
            "lastName": "Doe",
            "userEmail": "john.doe@example.com",
            "phoneNumber": 712345678,
            "password": "securepassword"
        }
        result = client.execute(mutation, variables=variables)

        assert "errors" not in result
        data = result["data"]["createUser"]["user"]
        assert data["user_id"] == "12345678"
        assert data["first_name"] == "John"
        assert data["last_name"] == "Doe"
        assert data["email"] == "john.doe@example.com"
        assert data["phone_number"] == 712345678
