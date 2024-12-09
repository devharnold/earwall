#transaction mutation test file
import pytest
from graphene.test import Client
from apis.v1.graphql.schema import Mutation
from unittest.mock import patch, MagicMock

class MutationTest:
    """Tests for our graphql mutation class"""
    @pytest.fixture
    def mocked_db_connection():
        """Mock the database connection"""
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value
        yield mock_conn, mock_cursor

    @pytest.fixture
    def client():
        """Graphene test client for executing mutations"""
        return Client(schema=Mutation)
    
    def test_transaction_mutation(client, mocked_db_connection):
        #Mocked exchange rate from usd to gbp
        EXCHANGE_RATE_USD_TO_GBP = 0.78

        amount_in_usd = 5.00
        amount_in_gbp = round(amount_in_usd * EXCHANGE_RATE_USD_TO_GBP, 2)

        mock_conn, mock_cursor = mocked_db_connection()
        mock_cursor.fetchone.return_value = {
            "user_ids": ["12345678", "87654321"],
            "user_emails": ["john.doe@example.com", "doe.john@example.com"],
            "cashwallet_ids": ["34454563432", "01004507100"],
            "transaction_id": "muxcv4554t9",
            "transaction_type": "multi-currency-p2p",
            "amount": {
                "original_currency": "USD",
                "original_amount": amount_in_usd,
                "converted_currency": "GBP",
                "converted_amount": amount_in_gbp
            }
        }

    mutation = """
    mutation createTransaction($userIds: Int!, $cashwalletIds: Int!, transactionId: Int!, transactionType: String!, amount: Float!) {
        createTransaction(userIds: $userIds, cashwalletIds: $cashwalletIds, transactionId: $transactionId, transactionType: $transactionType, amount: $amount) {
            transaction {
                user_id
                cashwallet_ids
                transaction_id
                transaction_type
                amount
            }
        }
    }
    """
    variables = {
        "userIds": ["12345678", "87654321"],
        "cashwalletIds": ["34454563432", "01004507100"],
        "transactionId": "muxcv4554t9",
        "transaction_type": "multi-currency-p2p",
        "amount": 5.00
    }
    result = client.execute(mutation, variables=variables)

    assert "errors" not in result
    data = result["data"]["createTransaction"]["transaction"]
    assert data["user_ids"] == ["12345678", "87654321"]
    assert data["cashwallet_ids"] == ["34454563432", "01004507100"]
    assert data["transaction_id"] == "muxcv4554t9"
    assert data["transaction_type"] == "multi-currency-p2p"
    assert data["amount"] == 5.00