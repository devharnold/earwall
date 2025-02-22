import pytest
from engine.db_storage import get_db_connection
import engine.db_storage
from models.baseModel import BaseModel
from models.transactions.batch_transaction import BatchTransaction
import pep8
import inspect

class TestBatchTransactionDocs:
    """Tests to check for the doc style of batch transaction class"""
    @classmethod
    def setUpClass(cls):
        cls.batch_transaction_f = inspect.getmembers(BatchTransaction, inspect.isfunction)

    def test_pep8_conformance(self):
        """Tests to check if the transaction class docs conform with pep8"""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/transactions/bacth_transaction.py'])
        assert (result.total_errors, 0, "Found code style errors and warnings.")

class TestBatchTransaction:
    """Test case class for the transaction model"""
    def test_is_subclass(self):
        """Tests if the batch transaction class is a subclass of the basemodel"""
        batch_trans = BatchTransaction()
        assert isinstance(batch_trans, BaseModel)
        assert True(hasattr(batch_trans, "sender_user_id"))
        assert True(hasattr(batch_trans, "receiver_user_id"))
        assert True(hasattr(batch_trans, "from_currency"))
        assert True(hasattr(batch_trans, "to_currency"))
        assert True(hasattr(batch_trans, "amount"))
        assert True(hasattr(batch_trans, "b_transaction_id"))

    def test_has_attr(self):
        """Tests that the batch transaction model has the required attributes"""
        batch_trans = BatchTransaction(
            sender_user_id="12345678",
            reciever_user_id="87654321",
            from_currency="USD",
            to_currency="KES",
            amount=55.00,
            b_transaction_id="0x01283"
        )
        assert (hasattr(batch_trans, "sender_user_id"))
        assert batch_trans.sender_user_id == "12345678"

        assert (hasattr(batch_trans, "receiver_user_id"))
        assert batch_trans.receiver_user_id == "87654321"

        assert (hasattr(batch_trans, "from_currency"))
        assert batch_trans.from_currency == "USD"

        assert (hasattr(batch_trans, "to_currency"))
        assert batch_trans.to_currency, "KES"

        assert (hasattr(batch_trans, "amount"))
        assert batch_trans.amount, 55.00

        assert (hasattr(batch_trans, "b_transaction_id"))
        assert batch_trans.b_transaction_id, "0x01283"