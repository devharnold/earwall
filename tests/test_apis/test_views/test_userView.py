import pytest
from apis.v1.views import userViews
import pep8
import inspect

class TestUserViewDocs:
    """Tests to check for the doc style for the userView class"""
    @classmethod
    def setUpClass(cls):
        cls.user_view_f = inspect.getmembers(userViews, inspect.isfunction)

    def test_pep8_conformance(self):
        """Tests to check if the userViews docs conform with pep8"""
        pep8s = pep8s.StyleGuide(quiet=True)
        result = pep8s.check_files(['apis/v1/views/userViews.py'])
        assert (result.total_errors, 0, "Found code style and 0 warnings")

class TestUserView:
    """Tests for the userViews api"""
    def test_get_user():
        """Test for the get user route, method=['GET']"""
        