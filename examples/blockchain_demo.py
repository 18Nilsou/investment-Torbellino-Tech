import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from market_sim.blockchain.blockchain import Blockchain
from market_sim.blockchain.consensus.pow import PowConsensus
from market_sim.blockchain.ethereum.ethereum_network import EthereumNetwork
from market_sim.blockchain.contracts.trade_contract import TradeContract
from market_sim.analysis.visualization.blockchain_viz import BlockchainVisualizer

def run_demo():
    print("Blockchain Integration Demo")
    print("--------------------------")
    
    # Create a blockchain with PoW consensus
    blockchain = Blockchain(consensus_mechanism=PowConsensus(difficulty=2))
    
    # Add some transactions
    print("Adding transactions to blockchain...")
    blockchain.add_transaction({"from": "Alice", "to": "Bob", "amount": 50})
    blockchain.add_transaction({"from": "Bob", "to": "Charlie", "amount": 30})
    blockchain.add_transaction({"from": "Charlie", "to": "Alice", "amount": 20})
    
    # Mine a block
    print("Mining block...")
    block = blockchain.mine_pending_transactions("miner1")
    print(f"Block mined: {block.hash}")
    
    # Add more transactions
    blockchain.add_transaction({"from": "Alice", "to": "David", "amount": 10})
    blockchain.add_transaction({"from": "David", "to": "Bob", "amount": 5})
    block = blockchain.mine_pending_transactions("miner2")
    print(f"Block mined: {block.hash}")
    
    # Validate blockchain
    print(f"Is blockchain valid? {blockchain.is_chain_valid()}")
    
    # Ethereum network simulation
    print("\nEthereum Network Simulation")
    print("--------------------------")
    eth_network = EthereumNetwork()
    
    # Create accounts
    alice = eth_network.create_account()
    bob = eth_network.create_account()
    
    print(f"Alice's address: {alice.address}")
    print(f"Bob's address: {bob.address}")
    
    # Fund accounts
    alice.balance = 100
    print(f"Funded Alice with 100 ETH")
    
    # Transfer ETH
    eth_network.transfer(alice.address, bob.address, 50)
    print(f"Transferred 50 ETH from Alice to Bob")
    print(f"Alice's balance: {alice.balance}")
    print(f"Bob's balance: {bob.balance}")
    
    # Deploy contract
    contract_addr = eth_network.deploy_contract(alice.address, "sample contract code")
    print(f"Deployed contract at address: {contract_addr}")
    
    # Smart contract demo
    print("\nSmart Contract Demo")
    print("-----------------")
    trade_contract = TradeContract("0xTradeContract", "market_operator")
    
    # Deposit funds
    trade_contract.deposit({"amount": 100}, "trader1")
    trade_contract.deposit({"amount": 100}, "trader2")
    print("Traders deposited funds to contract")
    
    # Place orders
    buy_id = trade_contract.place_order({"type": "buy", "price": 10, "amount": 5}, "trader1")
    sell_id = trade_contract.place_order({"type": "sell", "price": 10, "amount": 5}, "trader2")
    print(f"Buy order placed with ID: {buy_id}")
    print(f"Sell order placed with ID: {sell_id}")
    
    # Execute trade
    trade_id = trade_contract.execute_trade({
        "buy_order_id": buy_id,
        "sell_order_id": sell_id,
        "amount": 5,
        "price": 10,
        "timestamp": 123456789
    }, "market_operator")
    print(f"Trade executed with ID: {trade_id}")
    
    # Visualize blockchain
    print("\nGenerating blockchain visualizations...")
    visualizer = BlockchainVisualizer(blockchain)
    visualizer.plot_chain_structure()
    visualizer.plot_transaction_volume()
    print("Visualizations saved!")

if __name__ == "__main__":
    run_demo()