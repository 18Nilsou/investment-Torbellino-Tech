import hashlib
import time
from typing import List, Dict, Any, Optional

class Block:
    def __init__(self, index: int, timestamp: float, transactions: List[Dict], 
                 previous_hash: str, nonce: int = 0):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()
        
    def calculate_hash(self) -> str:
        """Calculate SHA-256 hash of the block."""
        block_string = (f"{self.index}{self.timestamp}{self.transactions}"
                        f"{self.previous_hash}{self.nonce}")
        return hashlib.sha256(block_string.encode()).hexdigest()
        
class Blockchain:
    def __init__(self, consensus_mechanism=None):
        """Initialize blockchain with genesis block."""
        self.chain = [self._create_genesis_block()]
        self.pending_transactions = []
        self.consensus = consensus_mechanism
        
    def _create_genesis_block(self) -> Block:
        """Create the first block in the chain."""
        return Block(0, time.time(), [], "0")
        
    def get_latest_block(self) -> Block:
        """Return the most recent block."""
        return self.chain[-1]
        
    def add_transaction(self, transaction: Dict[str, Any]) -> int:
        """Add a transaction to the pending list."""
        self.pending_transactions.append(transaction)
        return self.get_latest_block().index + 1
        
    def mine_pending_transactions(self, miner_address: str) -> Optional[Block]:
        """Mine pending transactions and add a new block to the chain."""
        if not self.pending_transactions:
            return None
            
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            transactions=self.pending_transactions,
            previous_hash=self.get_latest_block().hash
        )
        
        if self.consensus:
            new_block = self.consensus.find_consensus(new_block)
        
        # Add block to chain and clear pending transactions
        self.chain.append(new_block)
        self.pending_transactions = []
        
        return new_block
        
    def is_chain_valid(self) -> bool:
        """Verify the blockchain integrity."""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            
            # Check hash integrity
            if current.hash != current.calculate_hash():
                return False
                
            # Check hash linkage
            if current.previous_hash != previous.hash:
                return False
                
        return True