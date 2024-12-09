#cashwallet query test file
import pytest
from unittest.mock import patch, MagicMock
from graphene import Schema
from apis.v1.graphql.queries import Query
from apis.v1.graphql.types import UserType

class CashWalletTestQuery:
    @pytest.fixture
    def mock_db_connection():
        """Fixture that mocks the db connection"""
        mock_conn, mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        return mock_cursor, mock_conn
    
    @patch('engine.db_storage.get_db_connection')
    def test_resolve_cashwallet(mock_get_db_connection, mock_db_connection):
        """Test cashwallet query"""
        mock_get_db_connection.return_value = mock_db_connection[0]
        mock_cursor = mock_db_connection[1]

        mock_cursor.fetchone.return_value = [
            (0101112, 12345678, 55.00)
        ]

        query = '''
        query {
            cashwallet(id: 0101112) {
                cashwallet_id
                user_id
                balance
            }
        }
        '''
        schema = Schema(query=Query)
        result = schema.execute(query)

        assert result.errors is None
        assert len(result.data['cashwallet']) == 1
        assert result.data['cashwallet'][0]['cashwallet_id'] == 0101112
        assert result.data['cashwallet'][0]['user_id'] == 12345678
        assert result.data['cashwallet'][0]['balance'] == 55.00

    @patch('engine.db_storage.get_db_connection')
    def test_resolve_cashwallet_with_error(mock_get_db_connection):
        """Tests what happens with this function after the connection fails"""
        mock_get_db_connection.side_effect = Exception("Database connection failed")

        query='''
        query {
            cashwallet(id: 453423232) {
                cashwallet_id
                user_id
                balance
            }
        }
        '''

        schema = Schema(query=Query)
        result = schema.execute(query)

        assert result.errors is not None
        assert result.errors[0].message == "Cannot get any cashwallet"