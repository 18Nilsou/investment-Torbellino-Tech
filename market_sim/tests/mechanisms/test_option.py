import unittest
import pytest
from market_sim.market.mechanisms.options import Option
from datetime import datetime

class TestOption(unittest.TestCase):
    def setUp(self):
        self.call_option = Option(strike_price=100, expiry_date="2025-12-31", option_type="call", premium=5)
        self.put_option = Option(strike_price=100, expiry_date="2025-12-31", option_type="put", premium=5)

    def test_is_expired(self):
        self.assertFalse(self.call_option.is_expired(datetime(2025, 5, 20)))
        self.assertTrue(self.call_option.is_expired(datetime(2026, 1, 1)))

    def test_calculate_payoff_call(self):
        self.assertEqual(self.call_option.calculate_payoff(120), 15)  # (120 - 100) - 5
        self.assertEqual(self.call_option.calculate_payoff(90), -5)  # No payoff, only premium loss

    def test_calculate_payoff_put(self):
        self.assertEqual(self.put_option.calculate_payoff(80), 15)  # (100 - 80) - 5
        self.assertEqual(self.put_option.calculate_payoff(110), -5)  # No payoff, only premium loss

if __name__ == "__main__":
    unittest.main()