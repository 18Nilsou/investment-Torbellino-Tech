import unittest
from market_sim.blockchain.contracts.trade_contract import TradeContract

class TestTradeContract(unittest.TestCase):
    def setUp(self):
        self.contract = TradeContract("0x123", "owner")
        
    def test_deposit(self):
        """Test depositing funds to the contract."""
        result = self.contract.deposit({"amount": 100}, "user1")
        self.assertTrue(result)
        self.assertEqual(self.contract.state["balances"]["user1"], 100)
        
    def test_withdraw(self):
        """Test withdrawing funds from the contract."""
        # Deposit first
        self.contract.deposit({"amount": 100}, "user1")
        
        # Withdraw valid amount
        result = self.contract.withdraw({"amount": 50}, "user1")
        self.assertTrue(result)
        self.assertEqual(self.contract.state["balances"]["user1"], 50)
        
        # Attempt to withdraw too much
        result = self.contract.withdraw({"amount": 100}, "user1")
        self.assertFalse(result)
        self.assertEqual(self.contract.state["balances"]["user1"], 50)
        
    def test_place_order(self):
        """Test placing a trading order."""
        # Deposit funds first
        self.contract.deposit({"amount": 100}, "user1")
        
        # Place order
        order_params = {
            "type": "buy",
            "price": 10,
            "amount": 5
        }
        order_id = self.contract.place_order(order_params, "user1")
        
        self.assertEqual(order_id, 0)  # First order should have ID 0
        self.assertEqual(len(self.contract.state["orders"]), 1)
        self.assertEqual(self.contract.state["orders"][0]["type"], "buy")
        
    def test_execute_trade(self):
        """Test executing a trade between orders."""
        # Setup
        self.contract.deposit({"amount": 100}, "buyer")
        self.contract.deposit({"amount": 100}, "seller")
        
        buy_order_id = self.contract.place_order({
            "type": "buy", "price": 10, "amount": 5
        }, "buyer")
        
        sell_order_id = self.contract.place_order({
            "type": "sell", "price": 10, "amount": 5
        }, "seller")
        
        # Execute trade by owner
        trade_params = {
            "buy_order_id": buy_order_id,
            "sell_order_id": sell_order_id,
            "amount": 5,
            "price": 10,
            "timestamp": 123456789
        }
        
        trade_id = self.contract.execute_trade(trade_params, "owner")
        
        self.assertEqual(trade_id, 0)  # First trade should have ID 0
        self.assertEqual(len(self.contract.state["trades"]), 1)
        self.assertEqual(self.contract.state["trades"][0]["buyer"], "buyer")
        self.assertEqual(self.contract.state["trades"][0]["seller"], "seller")
        
        # Check order status
        self.assertEqual(self.contract.state["orders"][buy_order_id]["status"], "filled")
        self.assertEqual(self.contract.state["orders"][sell_order_id]["status"], "filled")

if __name__ == "__main__":
    unittest.main()