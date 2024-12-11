import pytest
from unittest.mock import patch, MagicMock
from graphene import Schema
from apis.v1.graphql.queries import Query

@pytest.fixture
def mock_db_connection():
    """Fixture that mocks the db connection"""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn, mock_cursor

class TestUserQuery:
    @patch('engine.db_storage.get_db_connection')
    def test_resolve_user(self, mock_get_db_connection, mock_db_connection):
        """Test for the resolve user function"""
        mock_get_db_connection.return_value = mock_db_connection[0]
        mock_cursor = mock_db_connection[1]

        # Setup the mock cursor to return a pre-defined user
        mock_cursor.fetchone.return_value = (12345678, 'John', 'Doe', 'john.doe@example.com')

        query = '''
        query {
            user(userId: 12345678) {
                userId
                firstName
                lastName
                email
            }
        }
        '''

        # Execute the GraphQL query
        schema = Schema(query=Query)
        result = schema.execute(query)

        assert result.errors is None
        assert result.data['user'] is not None
        assert result.data['user']['userId'] == 12345678
        assert result.data['user']['firstName'] == 'John'
        assert result.data['user']['lastName'] == 'Doe'
        assert result.data['user']['email'] == 'john.doe@example.com'

    @patch('engine.db_storage.get_db_connection')
    def test_resolve_user_with_error(self, mock_get_db_connection):
        """Test for what happens in resolve_user when the connection fails"""
        mock_get_db_connection.side_effect = Exception("Database connection failed")

        query = '''
        query {
            user(userId: 1) {
                userId
                firstName
                lastName
                email
            }
        }
        '''

        schema = Schema(query=Query)
        result = schema.execute(query)

        assert result.errors is not None
        assert "Cannot get users" in str(result.errors[0])
