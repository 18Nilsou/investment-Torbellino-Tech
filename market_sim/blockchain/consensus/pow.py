from typing import Any

class PowConsensus:
    """Proof of Work consensus mechanism."""
    
    def __init__(self, difficulty: int = 4):
        self.difficulty = difficulty
        
    def find_consensus(self, block: Any) -> Any:
        """Mine a block using proof of work."""
        target = '0' * self.difficulty
        
        while block.hash[:self.difficulty] != target:
            block.nonce += 1
            block.hash = block.calculate_hash()
            
        return block