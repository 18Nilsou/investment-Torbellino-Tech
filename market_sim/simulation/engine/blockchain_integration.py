from typing import Dict, List, Any
from market_sim.blockchain.blockchain import Blockchain
from market_sim.blockchain.ethereum.ethereum_network import EthereumNetwork
from market_sim.blockchain.contracts.trade_contract import TradeContract

class BlockchainIntegration:
    """Integration between market simulation and blockchain."""
    
    def __init__(self, simulation):
        self.simulation = simulation
        self.blockchain = Blockchain()
        self.ethereum = EthereumNetwork()
        self.trade_contracts = {}
        self.trade_history = []
        
    def setup_ethereum_accounts(self, agents):
        """Create Ethereum accounts for all trading agents."""
        for agent_id, agent in agents.items():
            account = self.ethereum.create_account()
            # Fund the account with initial balance
            account.balance = 1000
            agent.ethereum_address = account.address
            
    def deploy_trade_contract(self, symbol):
        """Deploy a trading contract for a specific symbol."""
        owner_address = "market_operator"
        
        # Ensure market operator has an account
        if owner_address not in self.ethereum.accounts:
            account = self.ethereum.create_account()
            account.address = owner_address
            account.balance = 10000
            self.ethereum.accounts[owner_address] = account
            
        # Deploy contract
        contract_address = f"contract_{symbol}"
        self.trade_contracts[symbol] = TradeContract(contract_address, owner_address)
        
        return contract_address
        
    def record_trade_on_blockchain(self, trade):
        """Record a trade on the blockchain."""
        # Add trade to pending transactions
        trade_data = {
            "symbol": trade.symbol,
            "price": trade.price,
            "quantity": trade.quantity,
            "buyer": trade.buyer,
            "seller": trade.seller,
            "timestamp": trade.timestamp
        }
        
        self.blockchain.add_transaction(trade_data)
        
        # Record trade in appropriate contract
        if trade.symbol not in self.trade_contracts:
            self.deploy_trade_contract(trade.symbol)
            
        contract = self.trade_contracts[trade.symbol]
        
        # Find or create orders in contract
        buy_order_id = contract.place_order({
            "type": "buy",
            "price": trade.price,
            "amount": trade.quantity
        }, trade.buyer)
        
        sell_order_id = contract.place_order({
            "type": "sell",
            "price": trade.price,
            "amount": trade.quantity
        }, trade.seller)
        
        # Execute trade in contract
        contract.execute_trade({
            "buy_order_id": buy_order_id,
            "sell_order_id": sell_order_id,
            "amount": trade.quantity,
            "price": trade.price,
            "timestamp": trade.timestamp
        }, contract.owner)
        
        self.trade_history.append(trade_data)
        
    def mine_block(self, miner_address="market_operator"):
        """Mine a new block with pending transactions."""
        return self.blockchain.mine_pending_transactions(miner_address)
        
    def get_trade_history(self, symbol=None):
        """Get trade history, optionally filtered by symbol."""
        if symbol is None:
            return self.trade_history
            
        return [trade for trade in self.trade_history if trade["symbol"] == symbol]