from .contract import SmartContract

class TradeContract(SmartContract):
    """Smart contract for trading assets."""
    
    def __init__(self, address: str, owner: str):
        super().__init__(address, owner)
        self.state = {
            "balances": {},
            "orders": [],
            "trades": []
        }
        
    def deposit(self, params, caller):
        """Deposit funds to the contract."""
        amount = params.get("amount", 0)
        if amount <= 0:
            return False
            
        if caller not in self.state["balances"]:
            self.state["balances"][caller] = 0
            
        self.state["balances"][caller] += amount
        return True
        
    def withdraw(self, params, caller):
        """Withdraw funds from the contract."""
        amount = params.get("amount", 0)
        if amount <= 0:
            return False
            
        if caller not in self.state["balances"] or self.state["balances"][caller] < amount:
            return False
            
        self.state["balances"][caller] -= amount
        return True
        
    def place_order(self, params, caller):
        """Place a trading order."""
        if caller not in self.state["balances"] or self.state["balances"][caller] <= 0:
            return False
            
        order_type = params.get("type")
        price = params.get("price")
        amount = params.get("amount")
        
        if not all([order_type, price, amount]):
            return False
            
        order = {
            "id": len(self.state["orders"]),
            "trader": caller,
            "type": order_type,
            "price": price,
            "amount": amount,
            "status": "open"
        }
        
        self.state["orders"].append(order)
        return order["id"]
        
    def execute_trade(self, params, caller):
        """Execute a trade between orders."""
        if caller != self.owner:  # Only contract owner can execute trades
            return False
            
        buy_order_id = params.get("buy_order_id")
        sell_order_id = params.get("sell_order_id")
        amount = params.get("amount")
        price = params.get("price")
        
        # Validate orders existence
        valid_orders = all([
            0 <= buy_order_id < len(self.state["orders"]),
            0 <= sell_order_id < len(self.state["orders"])
        ])
        
        if not valid_orders:
            return False
            
        buy_order = self.state["orders"][buy_order_id]
        sell_order = self.state["orders"][sell_order_id]
        
        # Record the trade
        trade = {
            "id": len(self.state["trades"]),
            "buyer": buy_order["trader"],
            "seller": sell_order["trader"],
            "price": price,
            "amount": amount,
            "timestamp": params.get("timestamp")
        }
        
        self.state["trades"].append(trade)
        
        # Update order statuses
        buy_order["status"] = "filled" if buy_order["amount"] <= amount else "partial"
        sell_order["status"] = "filled" if sell_order["amount"] <= amount else "partial"
        
        return trade["id"]