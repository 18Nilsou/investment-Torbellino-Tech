from market_sim.blockchain.blockchain import Blockchain
from market_sim.blockchain.consensus.pow import PowConsensus
from market_sim.analysis.visualization.blockchain_viz import BlockchainVisualizer

def run_visualization_demo():
    """Run a demo to visualize blockchain state and test results."""
    # Create and populate blockchain
    blockchain = Blockchain(consensus_mechanism=PowConsensus(difficulty=2))
    
    # Add transactions in batches to create multiple blocks
    for batch in range(3):
        for i in range(10):
            blockchain.add_transaction({
                "from": f"user{i}",
                "to": f"user{i+1}",
                "amount": 50 + i * 10,
                "batch": batch
            })
        blockchain.mine_pending_transactions(f"miner{batch}")
        
    # Create visualizations
    print("Creating blockchain visualizations...")
    visualizer = BlockchainVisualizer(blockchain)
    visualizer.plot_chain_structure()
    visualizer.plot_transaction_volume()
    
    print(f"Blockchain created with {len(blockchain.chain)} blocks")
    print(f"Genesis block + {len(blockchain.chain)-1} mined blocks")
    print("Visualizations saved to blockchain_structure.png and transaction_volume.png")

if __name__ == "__main__":
    run_visualization_demo()