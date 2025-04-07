#!/usr/bin/env python3
#test cash_wallet file

import pytest
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
        cash_wallet = CashWallet(
            cashwallet_id="12345678",
            user_email="john.doe@example.com",
            user_id="34wses43",
            password="securepass",
            balance=0.00,
            currency="USD",
        )

        assert (hasattr(cash_wallet, "cashwallet_id"))
        assert len(cash_wallet.cashwallet_id) == 8

        assert (hasattr(cash_wallet, "user_id"))
        assert len(cash_wallet.user_id) == 8

        assert (hasattr(cash_wallet, "user_email"))
        assert cash_wallet.password == "securepass"

        assert (hasattr(cash_wallet, "balance"))
        assert cash_wallet.balance == 0.00
