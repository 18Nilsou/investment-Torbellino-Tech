import matplotlib.pyplot as plt
import networkx as nx
from datetime import datetime
import matplotlib.dates as mdates

class BlockchainVisualizer:
    """Visualization tools for blockchain data."""
    
    def __init__(self, blockchain):
        self.blockchain = blockchain
        
    def plot_chain_structure(self, figsize=(12, 8)):
        """Visualize the blockchain structure as a directed graph."""
        G = nx.DiGraph()
        
        # Add nodes for each block
        for block in self.blockchain.chain:
            G.add_node(block.hash[:10], 
                      label=f"Block {block.index}\n{len(block.transactions)} txns")
            
            # Add edge from previous block
            if block.index > 0:
                G.add_edge(block.previous_hash[:10], block.hash[:10])
        
        plt.figure(figsize=figsize)
        pos = nx.spring_layout(G)
        
        # Draw nodes and edges
        nx.draw_networkx_nodes(G, pos, node_color="skyblue", node_size=1500)
        nx.draw_networkx_edges(G, pos, arrowsize=20, width=2)
        nx.draw_networkx_labels(G, pos, labels=nx.get_node_attributes(G, 'label'))
        
        plt.title("Blockchain Structure")
        plt.axis('off')
        plt.tight_layout()
        plt.savefig("blockchain_structure.png")
        plt.close()
        
    def plot_transaction_volume(self, figsize=(10, 6)):
        """Plot transaction volume over time."""
        timestamps = []
        tx_counts = []
        
        for block in self.blockchain.chain:
            if block.index > 0:  # Skip genesis block
                timestamps.append(datetime.fromtimestamp(block.timestamp))
                tx_counts.append(len(block.transactions))
        
        plt.figure(figsize=figsize)
        plt.plot(timestamps, tx_counts, 'o-', linewidth=2, markersize=8)
        
        plt.gcf().autofmt_xdate()
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
        
        plt.title("Transaction Volume Over Time")
        plt.xlabel("Time")
        plt.ylabel("Number of Transactions")
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig("transaction_volume.png")
        plt.close()