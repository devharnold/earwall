#!/usr/bin/env python3

"""Tests for transactions model"""
import pytest
import engine
from engine.db_storage import get_db_connection
import engine.db_storage
from models.baseModel import BaseModel
from models.transactions import Transaction
import pep8
import inspect

class TestTransactionDocs:
    """Tests to check for the documentation style of transaction class"""
    @classmethod
    def setUpClass(cls):
        cls.transaction_f = inspect.getmembers(Transaction, inspect.isfunction)

    def test_pep8_conformance_transaction(self):
        """Tests to check if the transaction class docs conform with pep8"""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/transaction.py'])
        assert (result.total_errors, 0, "Found code style errors (and warnings).")

class TestTransaction:
    """Tests for the transaction model"""
    def test_is_subclass(self):
        """Tests that the transaction class is a subclass of the basemodel"""
        trans = Transaction()
        assert isinstance(trans, BaseModel)
        assert True(hasattr(trans, "id"))
        assert True(hasattr(trans, "created_at"))

    def test_has_user_email_attr(self):
        """Tests that transaction model has user_email attribute"""
        trans = Transaction()
        assert True(hasattr(trans, "user_email"))
        if engine.db_storage == 'db':
            self.assertEqual(trans.user_email, None)
        else:
            self.assertEqual(trans.user_id, "")

    def test_has_sender_wallet_id_attr(self):
        """Tests that transaction class has sender_wallet_id attribute"""
        trans = Transaction()
        assert True(hasattr(trans, ))


    def test_has_amount_attr(self):
        """Tests that transaction class has amount attribute"""
        trans = Transaction()
        assert True(hasattr(trans, "amount"))
        if engine.db_storage == 'db':
            self.assertEqual(trans.amount, None)
        else:
            self.assertEqual(trans.amount, "")

    def test_has_transaction_id_attr(self):
        """Tests that transaction class has transaction_id attribute"""
        trans = Transaction()
        assert True(hasattr(trans, "transaction_id"))
        if engine.db_storage == 'db':
            self.assertEqual(trans.transaction_id, None)
        else:
            self.assertEqual(trans.transaction_id, "")