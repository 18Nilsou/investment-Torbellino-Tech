import pytest
from market_sim.blockchain.contracts.trade_contract import TradeContract

class TestTradeContract:
    @pytest.fixture
    def contract(self):
        return TradeContract("0x123", "owner")
    
    def test_deposit(self, contract):
        """Test depositing funds."""
        result = contract.deposit({"amount": 100}, "user1")
        assert result is True
        assert contract.state["balances"]["user1"] == 100
    
    def test_withdraw(self, contract):
        """Test withdrawing funds."""
        # Deposit first
        contract.deposit({"amount": 100}, "user1")
        
        # Withdraw valid amount
        result = contract.withdraw({"amount": 50}, "user1")
        assert result is True
        assert contract.state["balances"]["user1"] == 50
        
        # Try to withdraw too much
        result = contract.withdraw({"amount": 100}, "user1")
        assert result is False
        assert contract.state["balances"]["user1"] == 50
    
    def test_place_order(self, contract):
        """Test placing an order."""
        # Deposit funds
        contract.deposit({"amount": 100}, "user1")
        
        # Place order
        order_id = contract.place_order({
            "type": "buy",
            "price": 10,
            "amount": 5
        }, "user1")
        
        assert order_id == 0
        assert len(contract.state["orders"]) == 1
        assert contract.state["orders"][0]["type"] == "buy"
    
    def test_execute_trade(self, contract):
        """Test trade execution."""
        # Setup
        contract.deposit({"amount": 100}, "buyer")
        contract.deposit({"amount": 100}, "seller")
        
        buy_id = contract.place_order({"type": "buy", "price": 10, "amount": 5}, "buyer")
        sell_id = contract.place_order({"type": "sell", "price": 10, "amount": 5}, "seller")
        
        # Execute trade
        trade_id = contract.execute_trade({
            "buy_order_id": buy_id,
            "sell_order_id": sell_id,
            "amount": 5,
            "price": 10,
            "timestamp": 123456789
        }, "owner")
        
        assert trade_id == 0
        assert len(contract.state["trades"]) == 1
        assert contract.state["orders"][buy_id]["status"] == "filled"