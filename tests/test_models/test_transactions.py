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
        assert True(hasattr(trans, "transaction_id"))
        assert True(hasattr(trans, "sender_user_email"))
        assert True(hasattr(trans, "receiver_user_email"))
        assert True(hasattr(trans, "sender_user_id"))
        assert True(hasattr(trans, "receiver_user_id"))
        assert True(hasattr(trans, "sender_cw_id"))
        assert True(hasattr(trans, "receiver_cw_id"))
        assert True(hasattr(trans, "amount"))
        assert True(hasattr(trans, "sender_currency"))
        assert True(hasattr(trans, "receiver_currency"))
        assert True(hasattr(trans, "created_at"))

    def test_has_attr(self):
        """Tests that the transaction model has the user_email attr"""
        trans = Transaction(
            sender_user_email="john.doe@example.com",
            receiver_user_email="doe.john@example.com",
            sender_user_id="12345678",
            receiver_user_id="87654321",
            sender_cw_id="23232",
            receiver_cw_id="45772",
            amount=554.00,
            sender_currency="GBP",
            receiver_currency="USD",
            transaction_id="453223"
        )
        assert (hasattr(trans, "sender_user_email"))
        assert trans.sender_user_email == "john.doe@example.com"

        assert (hasattr(trans, "receiver_user_email"))
        assert trans.receiver_user_email == "doe.john@example.com"

        assert (hasattr(trans, "sender_user_id"))
        assert trans.sender_user_id == "12345678"

        assert (hasattr(trans, "receiver_user_id"))
        assert trans.receiver_user_id == "87654321"

        assert (hasattr(trans, "sender_cw_id"))
        assert trans.sender_cw_id == "23232"

        assert (hasattr(trans, "receiver_cw_id"))
        assert trans.receiver_cw_id == "45772"

        assert (hasattr(trans, "amount"))
        assert trans.amount == 554.00

        assert (hasattr(trans, "sender_currency"))
        assert trans.sender_currency == "GBP"

        assert (hasattr(trans, "receiver_currency"))
        assert trans.receiver_currency == "USD"

        assert (hasattr(trans, "transaction_id"))
        assert trans.transaction_id == "453223"