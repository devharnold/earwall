#!/usr/bin/env python3
#test cash_wallet file

import pytest
import engine
import engine.db_storage
from engine.db_storage import get_db_connection
from models.baseModel import BaseModel
from models.wallets.cashwallet import CashWallet
import pep8
from datetime import datetime
import inspect

class TestCashWalletDocs:
    """Test to check the documentation style of the cash wallet class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc test class"""
        cls.cash_wallet_f = inspect.getmembers(CashWallet, inspect.isfunction)

    def test_pep8_conformance_cash_wallet(self):
        """tests to check if the cash wallet class docs conforms to pep8"""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/wallets/cashwallet.py'])
        assert (result.total_errors, 0, "Found code style errors (and warnings).")

class TestCashWallet:
    """Tests for the cash wallet class"""
    def test_is_subclass(self):
        """tests that the cash wallet is a subclass of the basemodel"""
        cash_wallet = CashWallet()
        assert isinstance(cash_wallet, BaseModel)
        assert True(hasattr(cash_wallet, "id"))
        assert True(hasattr(cash_wallet, "created_at"))

    def test_has_user_id_attr(self):
        """tests that the cash wallet model has user id attribute"""
        cash_wallet = CashWallet()
        assert True(hasattr(cash_wallet, "user_id"))
        if engine.db_storage == 'db':
            self.assertEqual(cash_wallet.user_id, None)
        else:
            self.assertEqual(cash_wallet.user_id, "")

    def test_has_balance_attr(self):
        """tests that the cash wallet model has balance attribute"""
        cash_wallet = CashWallet()
        assert True(hasattr(cash_wallet, "balance"))
        if engine.db_storage == 'db':
            self.assertEqual(cash_wallet.balance, None)
        else:
            self.assertEqual(cash_wallet.balance, 0)


    def test_has_cashwallet_id_attr(self):
        """tests that the cash wallet model has the cashwallet_id attribute"""
        cash_wallet = CashWallet()
        assert True(hasattr(cash_wallet, "cashwallet_id"))
        if engine.db_storage == 'db':
            self.assertEqual(cash_wallet.cashwallet_id, None)
        else:
            self.assertEqual(cash_wallet.cashwallet_id, "")

    def test_has_currency_attr(self):
        """tests that the cashwallet has currecny attribute"""
        cash_wallet = CashWallet()
        assert True(hasattr(cash_wallet, "currency"))
        if engine.db_storage == 'db':
            self.assertEqual(cash_wallet.currency, None)
        else:
            self.assertEqual(cash_wallet.currency, "")

    def test_has_password_attr(self):
        """tests that the cashwallet has password attr"""
        cash_wallet = CashWallet()
        assert True(hasattr(cash_wallet, "password"))
        if engine.db_storage == 'db':
            self.assertEqual(cash_wallet.password, None)
        else:
            self.assertEqual(cash_wallet.password, "")