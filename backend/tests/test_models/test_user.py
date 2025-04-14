#!usr/bin/env python3
# test for the user model
from backend.models.baseModel import BaseModel
from backend.models.user import User
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
        assert (result.total_errors , 0, "Found code style errors (and warnings).")

class TestUser:
    """Tests for the user class"""
    def test_is_subclass(self):
        """tests that the user is a subclass of the basemodel"""
        user = User()
        assert isinstance(user, BaseModel)
        assert True(hasattr(user, "user_id"))
        assert True(hasattr(user, "first_name"))
        assert True(hasattr(user, "last_name"))
        assert True(hasattr(user, "user_email"))
        assert True(hasattr(user, "phone_number"))
        assert True(hasattr(user, "paypal_id"))
        assert True(hasattr(user, "paypal_email"))
        assert True(hasattr(user, 'created_at'))

    def test_has_attributes(self):
        """tests that the user model has email attribute"""
        user = User(
            user_id="7e168958",
            first_name="John",
            last_name="Doe",
            user_email="john.doe@example.com",
            paypal_email="johndoe@paypal.com",
            phone_number="+2547433943",
            paypal_id="12234334",
            password="securepass123"
        )
        assert (hasattr(user, "user_id"))
        assert len(user.user_id) == 8

        assert (hasattr(user, "first_name"))
        assert user.first_name == "John"
        
        assert (hasattr(user, "last_name"))
        assert user.last_name == "Doe"

        assert (hasattr(user, "user_email"))
        assert user.user_email=="john.doe@example.com"

        assert (hasattr(user, "paypal_email"))
        assert user.paypal_email == "johndoe@paypal.com"

        assert (hasattr(user, "paypal_id"))
        assert user.paypal_id == "12234334"

        assert (hasattr(user, "password"))
        assert user.password == "securepass123"