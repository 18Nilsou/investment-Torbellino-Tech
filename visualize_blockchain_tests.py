import sys
import time
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

from market_sim.blockchain.blockchain import Blockchain
from market_sim.blockchain.consensus.pow import PowConsensus
from market_sim.blockchain.consensus.pos import PoSConsensus
from market_sim.blockchain.consensus.pbft import PBFTConsensus
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

def compare_consensus_mechanisms():
    """Compare different consensus mechanisms performance and characteristics."""
    print("Comparing consensus mechanisms...")
    
    # Parameters
    num_transactions = 50
    num_blocks = 3
    
    # Initialize blockchains with different consensus mechanisms
    pow_blockchain = Blockchain(consensus_mechanism=PowConsensus(difficulty=2))
    pos_blockchain = Blockchain(consensus_mechanism=PoSConsensus())
    pbft_blockchain = Blockchain(consensus_mechanism=PBFTConsensus(num_validators=4))
    
    # Add validators for PoS
    validators = ["validator1", "validator2", "validator3", "validator4"]
    stakes = [100, 200, 150, 300]
    for v, s in zip(validators, stakes):
        pos_blockchain.consensus.add_validator(v, s)
    
    # Process same transactions through different consensus mechanisms
    pow_times = []
    pos_times = []
    pbft_times = []
    
    for block in range(num_blocks):
        # Generate transactions
        transactions = [
            {"from": f"user{i}", "to": f"user{i+1}", "amount": 50 + i * 10}
            for i in range(num_transactions)
        ]
        
        # Process with PoW
        for tx in transactions:
            pow_blockchain.add_transaction(tx.copy())
        start_time = time.time()
        pow_blockchain.mine_pending_transactions(f"miner{block}")
        pow_times.append(time.time() - start_time)
        
        # Process with PoS
        for tx in transactions:
            pos_blockchain.add_transaction(tx.copy())
        start_time = time.time()
        pos_blockchain.mine_pending_transactions(f"validator{block % 4}")
        pos_times.append(time.time() - start_time)
        
        # Process with PBFT
        for tx in transactions:
            pbft_blockchain.add_transaction(tx.copy())
        start_time = time.time()
        pbft_blockchain.mine_pending_transactions("committee")
        pbft_times.append(time.time() - start_time)
    
    # Visualize comparison
    plot_consensus_comparison(pow_times, pos_times, pbft_times)
    
    return {
        "pow": pow_blockchain,
        "pos": pos_blockchain,
        "pbft": pbft_blockchain
    }

def plot_consensus_comparison(pow_times, pos_times, pbft_times):
    """Plot performance comparison between consensus mechanisms."""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x = np.arange(len(pow_times))
    width = 0.25
    
    ax.bar(x - width, pow_times, width, label='Proof of Work')
    ax.bar(x, pos_times, width, label='Proof of Stake')
    ax.bar(x + width, pbft_times, width, label='PBFT')
    
    ax.set_xlabel('Block Number')
    ax.set_ylabel('Block Mining Time (seconds)')
    ax.set_title('Consensus Mechanism Performance Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels([f'Block {i+1}' for i in range(len(pow_times))])
    ax.legend()
    
    plt.tight_layout()
    plt.savefig('consensus_comparison.png')
    plt.close()

def simulate_network_attacks():
    """Simulate common blockchain attacks and visualize their impact."""
    print("Simulating network attacks...")
    
    # Create blockchain for attack simulation
    blockchain = Blockchain(consensus_mechanism=PowConsensus(difficulty=1))
    
    # Add initial blocks
    for i in range(5):
        for j in range(5):
            blockchain.add_transaction({
                "from": f"honest_user{j}",
                "to": f"honest_user{j+1}",
                "amount": 100,
                "data": f"Legitimate transaction {i}-{j}"
            })
        blockchain.mine_pending_transactions("honest_miner")
    
    # Clone the blockchain for attack simulation
    honest_chain = blockchain.chain.copy()
    attack_chain = blockchain.chain[:3].copy()  # Start attack from block 3
    
    # Simulate 51% attack by creating alternative chain
    print("Simulating 51% attack...")
    for i in range(3):  # Create 3 malicious blocks
        for j in range(7):  # More transactions to make chain seem legitimate
            blockchain.add_transaction({
                "from": f"attacker{j}",
                "to": f"accomplice{j}",
                "amount": 999,  # Large suspicious amounts
                "data": f"Malicious transaction {i}-{j}"
            })
        malicious_block = blockchain.mine_pending_transactions("attacker")
        attack_chain.append(malicious_block)
    
    # Visualize blockchain before and after attack
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))
    
    # Honest chain visualization
    visualize_chain(honest_chain, ax1, "Honest Blockchain")
    
    # Attack chain visualization
    visualize_chain(attack_chain, ax2, "Attacker's Blockchain (51% Attack)")
    
    plt.tight_layout()
    plt.savefig("blockchain_attack_simulation.png")
    plt.close()

def simulate_fork_resolution():
    """Simulate a blockchain fork and its resolution."""
    print("Simulating fork resolution...")
    
    # Create main blockchain
    main_chain = Blockchain(consensus_mechanism=PowConsensus(difficulty=1))
    
    # Add initial blocks
    for i in range(3):
        for j in range(3):
            main_chain.add_transaction({
                "from": f"user{j}",
                "to": f"user{j+1}",
                "amount": 100,
                "data": f"Transaction {i}-{j}"
            })
        main_chain.mine_pending_transactions("miner1")
    
    # Create a fork - two miners find blocks at similar times
    fork_point = main_chain.chain.copy()
    
    # First fork
    fork1 = Blockchain(consensus_mechanism=PowConsensus(difficulty=1))
    fork1.chain = fork_point
    fork1.add_transaction({"from": "userA", "to": "userB", "amount": 200, "data": "Fork 1 transaction"})
    fork1.mine_pending_transactions("miner2")
    
    # Second fork
    fork2 = Blockchain(consensus_mechanism=PowConsensus(difficulty=1))
    fork2.chain = fork_point
    fork2.add_transaction({"from": "userC", "to": "userD", "amount": 300, "data": "Fork 2 transaction"})
    fork2.mine_pending_transactions("miner3")
    
    # Continue fork 1 (becomes the longest chain)
    for i in range(2):
        fork1.add_transaction({
            "from": f"userX{i}",
            "to": f"userY{i}",
            "amount": 50 + i * 10,
            "data": f"Fork 1 extended {i}"
        })
        fork1.mine_pending_transactions("miner2")
    
    # Visualize the fork
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 12))
    
    # Original chain
    visualize_chain(fork_point, ax1, "Original Chain Before Fork")
    
    # Fork 1 (longer chain)
    visualize_chain(fork1.chain, ax2, "Fork 1 (Becomes Main Chain - Longest Chain Rule)")
    
    # Fork 2 (shorter, will be orphaned)
    visualize_chain(fork2.chain, ax3, "Fork 2 (Orphaned Chain)")
    
    plt.tight_layout()
    plt.savefig("blockchain_fork_resolution.png")
    plt.close()

def visualize_chain(chain, ax, title):
    """Visualize a blockchain."""
    # Create nodes for each block
    block_positions = {i: (i, 0) for i in range(len(chain))}
    
    # Draw blocks
    for i, block in enumerate(chain):
        is_genesis = i == 0
        is_malicious = "attacker" in block.transactions[0]["from"] if block.transactions else False
        
        color = "lightblue" if is_genesis else "lightgreen"
        if is_malicious:
            color = "salmon"
        
        # Draw block
        block_rect = plt.Rectangle((i-0.4, -0.4), 0.8, 0.8, 
                                  color=color, alpha=0.8, 
                                  linewidth=2, edgecolor='black')
        ax.add_patch(block_rect)
        
        # Add block number
        ax.text(i, 0, f"Block {block.index}", ha='center', va='center', 
                fontweight='bold')
        
        # Add hash preview
        ax.text(i, -0.6, f"Hash: {block.hash[:10]}...", ha='center', va='center', 
                fontsize=8)
        
        # Connect blocks with arrows
        if i > 0:
            ax.annotate("", xy=(i-0.5, 0), xytext=(i-1+0.5, 0),
                       arrowprops=dict(arrowstyle="->", lw=2))
    
    # Set plot limits and title
    ax.set_xlim(-1, len(chain))
    ax.set_ylim(-1.5, 1)
    ax.set_title(title)
    ax.set_aspect('equal')
    ax.axis('off')

def simulate_pbft_consensus():
    """Simulate Practical Byzantine Fault Tolerance consensus."""
    print("Simulating PBFT consensus...")
    
    # Set up PBFT parameters
    num_nodes = 7
    byzantine_nodes = 2  # Faulty/malicious nodes
    
    # Need 2f+1 honest nodes for safety, where f is number of faulty nodes
    if num_nodes < 3 * byzantine_nodes + 1:
        print(f"Warning: System not safe with {num_nodes} nodes and {byzantine_nodes} faulty nodes")
        print(f"Need at least {3 * byzantine_nodes + 1} total nodes for safety")
    
    # Simulate consensus phases
    phases = ["PRE-PREPARE", "PREPARE", "COMMIT", "REPLY"]
    nodes = [f"Node {i+1}" for i in range(num_nodes)]
    
    # Select random byzantine nodes
    import random
    byzantine_indices = random.sample(range(num_nodes), byzantine_nodes)
    byzantine_node_names = [nodes[i] for i in byzantine_indices]
    
    # Visualize PBFT consensus
    fig, axes = plt.subplots(len(phases), 1, figsize=(12, 15))
    
    for phase_idx, phase in enumerate(phases):
        ax = axes[phase_idx]
        
        # Create a matrix of messages
        message_matrix = np.ones((num_nodes, num_nodes))
        
        # Byzantine nodes send conflicting messages
        for b_idx in byzantine_indices:
            for target in range(num_nodes):
                # Byzantine nodes might send conflicting messages to different nodes
                if random.random() < 0.7:  # 70% chance of sending wrong message
                    message_matrix[b_idx, target] = 0
        
        # Plot the message matrix
        im = ax.imshow(message_matrix, cmap='RdYlGn', vmin=0, vmax=1)
        
        # Add labels
        ax.set_xticks(np.arange(num_nodes))
        ax.set_yticks(np.arange(num_nodes))
        ax.set_xticklabels(nodes)
        ax.set_yticklabels(nodes)
        
        # Highlight byzantine nodes
        for b_name in byzantine_node_names:
            idx = nodes.index(b_name)
            ax.text(idx, -0.6, "Byzantine", color='red', ha='center')
        
        # Label rows and columns
        ax.set_xlabel("Message Recipients")
        ax.set_ylabel("Message Senders")
        ax.set_title(f"PBFT {phase} Phase - Message Consistency Matrix")
        
        # Rotate x labels
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    plt.colorbar(im, ax=axes, label="Message Consistency")
    plt.tight_layout()
    plt.savefig("pbft_consensus_simulation.png")
    plt.close()

def run_enhanced_visualization_demo():
    """Run enhanced blockchain visualization demos."""
    # Original blockchain visualization
    run_visualization_demo()
    
    # New visualizations
    blockchains = compare_consensus_mechanisms()
    simulate_network_attacks()
    simulate_fork_resolution()
    simulate_pbft_consensus()
    
    # Generate additional visualizations for PoS
    visualizer = BlockchainVisualizer(blockchains["pos"])
    visualizer.plot_chain_structure()
    visualizer.plot_transaction_volume()
    print("Enhanced visualizations created!")

if __name__ == "__main__":
    run_enhanced_visualization_demo()