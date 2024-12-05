#!usr/bin/env python3
# test for the user model
import pytest
import psycopg2
import engine
import engine.db_storage
from engine.db_storage import get_db_connection
from models.baseModel import BaseModel
from models.user import User
import pep8
from datetime import datetime
import inspect

class TestUserDocs:
    """Test to check the documentation style of the user class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc test class"""
        cls.user_f = inspect.getmembers(User, inspect.isfunction)

    def test_pep8_conformance_user(self):
        """tests to check if the user class docs conforms to pep8"""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/user.py'])
        assert (result.total_errors, 0, "Found code style errors (and warnings).")

class TestUser:
    """Tests for the user class"""
    def test_is_subclass(self):
        """tests that the user is a subclass of the basemodel"""
        user = User()
        assert isinstance(user, BaseModel)
        assert True(hasattr(user, "id"))
        assert True(hasattr(user, "created_at"))

    def test_has_email_attr(self):
        """tests that the user model has email attribute"""
        user = User()
        assert True(hasattr(user, "email"))
        if engine.db_storage == 'db':
            self.assertEqual(user.email, None)
        else:
            self.assertEqual(user.email, "")

    def test_has_first_name_attr(self):
        """tests that the user model has the first name attribute"""
        user = User()
        assert True(hasattr(user, "first_name"))
        if engine.db_storage == 'db':
            self.assertEqual(user.first_name, None)
        else:
            self.assertEqual(user.first_name, "")

    def test_has_last_name_attr(self):
        """tests that the user model has last name attribute"""
        user = User()
        assert True(hasattr(user, "last_name"))
        if engine.db_storage == 'db':
            self.assertEqual(user.last_name, None)
        else:
            self.assertEqual(user.last_name, "")

    def test_has_password_attr(self):
        """tests that the user model has password attribute"""
        user = User()
        assert True(hasattr(user, "password"))
        if engine.storage == 'db':
            self.assertEqual(user.password, None)
        else:
            self.assertEqual(user.password, "")