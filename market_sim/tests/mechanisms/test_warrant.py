import unittest
import pytest
from market_sim.market.mechanisms.warrants import Warrant
from datetime import datetime

class TestWarrant(unittest.TestCase):
    def setUp(self):
        self.warrant = Warrant(strike_price=50, expiry_date="2025-12-31", issuer="Company A", conversion_ratio=2, premium=3)

    def test_is_expired(self):
        self.assertFalse(self.warrant.is_expired(datetime(2025, 5, 20)))
        self.assertTrue(self.warrant.is_expired(datetime(2026, 1, 1)))

    def test_calculate_payoff(self):
        self.assertEqual(self.warrant.calculate_payoff(60), 17)  # ((60 - 50) * 2) - 3
        self.assertEqual(self.warrant.calculate_payoff(40), -3)  # No payoff, only premium loss

if __name__ == "__main__":
    unittest.main()