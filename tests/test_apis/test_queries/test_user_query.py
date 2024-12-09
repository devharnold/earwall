#user query test file
import pytest
from unittest.mock import patch, MagicMock
from graphene import Schema
from apis.v1.graphql.queries import Query
from apis.v1.graphql.types import UserType

class UserTestQuery:
    @pytest.fixture
    def mock_db_connection():
        """Fixture that mocks the db connection"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        return mock_conn, mock_cursor
    
    @patch('engine.db_storage.get_db_connection')
    def test_resolve_user(mock_get_db_connection, mock_db_connection):
        """Test for the resolve user function"""
        mock_get_db_connection.return_value = mock_db_connection[0]
        mock_cursor = mock_db_connection[1]

        #setup the mock cursor to return a pre-defined list of users
        mock_cursor.fetchall.return_value = [
            (12345678, 'John', 'Doe', 'john.doe@example.com'),
            (87654321, 'Doe', 'John', 'doe.john@example.com')
        ]

        query = '''
        query {
            user(id: 1) {
                user_id
                name
                email
            }
        }
        '''
        #execute the graphql query
        schema = Schema(query=Query)
        result = schema.execute(query)

        assert result.errors is None
        assert len(result.data['user']) == 2
        assert result.data['user'][0]['user_id'] == 12345678
        assert result.data['user'][0]['name'] == 'John Doe'
        assert result.data['user'][0]['email'] == 'john.doe@example.com'
        assert result.data['user'][1]['user_id'] == 87654321
        assert result.data['user'][1]['name'] == 'Doe John'
        assert result.data['user'][1]['email'] == 'doe.john@example.com'

    @patch('engine.db_storage.get_db_connection')
    def test_resolve_user_with_error(mock_get_db_connection):
        """Test for what happens for the resolve user function when the connection fails"""
        mock_get_db_connection.side_effect = Exception("Database connection failed")

        query='''
        query {
            user(id: 1) {
                user_id
                name
                email
            }
        }
        '''

        schema = Schema(query=Query)
        result = schema.execute(query)

        assert result.errors is not None
        assert result.errors[0].message == "Cannot get users"