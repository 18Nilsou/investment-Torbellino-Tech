import unittest
import pytest
from market_sim.market.mechanisms.marginAccount import MarginAccount

class TestMarginAccount(unittest.TestCase):
    def setUp(self):
        self.account = MarginAccount(initial_balance=1000, leverage_ratio=2)

    def test_borrow(self):
        self.account.borrow(500)
        self.assertEqual(self.account.balance, 1500)
        self.assertEqual(self.account.borrowed_funds, 500)

    def test_calculate_margin_call(self):
        self.account.borrow(500)
        self.assertFalse(self.account.calculate_margin_call(2000))  # Equity is sufficient
        self.assertTrue(self.account.calculate_margin_call(1000))  # Margin call triggered

    def test_liquidate(self):
        self.account.borrow(500)
        self.account.liquidate()
        self.assertEqual(self.account.balance, 0)
        self.assertEqual(self.account.borrowed_funds, 0)

if __name__ == "__main__":
    unittest.main()