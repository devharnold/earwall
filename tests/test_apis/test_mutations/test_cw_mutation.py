#test cashwallet mutation
from flask import Flask
import pytest
from graphene.test import Client
from apis.v1.graphql.schema import Mutation
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

class MutationTest:
    """Tests for our graphql mutation class"""
    @pytest.fixture
    def mocked_db_connection():
        """Mock the database connection"""
        mock_connection = MagicMock()
        mock_cursor = mock_connection.cursor.return_value
        yield mock_connection, mock_cursor

    @pytest.fixture
    def client():
        """Graphene test client for executing mutations"""
        return Client(schema=Mutation)
    
    def test_cashwallet_mutation(client, mocked_db_connection):
        mock_connection, mock_cursor = mocked_db_connection()
        mock_cursor.fetchone.return_value = {
            "user_id": "12345678",
            "cashwallet_id": "34454563432",
            "initial_balance": 0.00,
        }

        mutation = """
        mutation createCashWallet($userId: Int!, $cashwalletId: Int!, !initialBalance: Float!) {
            createCashWallet(userId: $userId, cashwalletId: $cashwalletId, initialBalance: $initialBalance) {
                cash_wallet {
                    user_id
                    cashwallet_id
                    initial_balance
                }
            }
        }
        """
        variables = {
            "userId": "12345678",
            "cashwalletId": "34454563432",
            "initialBalance": 0.00
        }
        result = client.execute(mutation, variables=variables)

        assert "errors" not in result
        data = result["data"]["createCashWallet"]["cash_wallet"]
        assert data["user_id"] == "12345678"
        assert data["cashwallet_id"] == "34454563432"
        assert data["initial_balance"] == 0.00


if __name__ == "__main__":
    app.run(debug=True)