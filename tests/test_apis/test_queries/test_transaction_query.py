import pytest
from unittest.mock import patch, MagicMock
from graphene import Schema
from apis.v1.graphql.queries import Query
from apis.v1.graphql.types import TransactionType

class TransactionTestQuery:
    @pytest.fixture
    def mock_db_connection():
        """Fixture to mock db connection"""
        mock_conn, mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        return mock_conn, mock_cursor
    
    @patch('engine.db_storage.get_db_connection')
    def test_resolve_transaction(mock_get_db_connection, mock_db_connection):
        """Test for the Transaction query"""
        mock_get_db_connection.return_value = mock_db_connection[0]
        mock_cursor = mock_db_connection[1]


        #setup the mock cursor to return a pre-defined transaction that took place
        mock_cursor.fetchone.return_value = [
            (0001, 1, 2, 0123, 001, 12.00)
        ]
        query = '''
        query {
            transaction(id: 0001) {
                transaction_id
                sender_user_id
                receiver_user_id
                sender_cw_id
                receiver_cw_id
                amount
            }
        }
        '''

        schema = Schema(query=Query)
        result = schema.execute(query)

        assert result.errors is None
        assert len(result.data['transaction']) == 1
        assert result.data['transaction'][0]['transaction_id'] == 0001
        assert result.data['sender'][0]['sender_user_id'] == 1
        assert result.data['receiver'][0]['receiver_user_id'] == 2
        assert result.data['cashwallet_id'][0]['sender_cashwallet_id'] == 0123
        assert result.data['cahwallet_id'][0]['receiver_cashwallet_id'] == 001
        assert result.data['amount'][0]['GBP'] == 12.00

    @patch('engine.db_storage.get_db_connection')
    def test_resolve_transaction_with_error(mock_get_db_connection):
        """Test for what happens after connection fails"""
        mock_get_db_connection.side_effect = Exception("Database connection failed")

        query='''
        query {
            transaction(id: 0001) {
                transaction_id
                sender_user_id
                receiver_user_id
                sender_cw_id
                receiver_cw_id
                amount
            }
        }
        '''

        schema = Schema(query=Query)
        result = schema.execute(query)

        assert result.errors is not None
        assert result.errors[0].message == "Cannot get any transaction"