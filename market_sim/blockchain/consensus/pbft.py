from typing import Dict, List, Any, Set
import hashlib
import time

class PBFTConsensus:
    """
    Practical Byzantine Fault Tolerance consensus mechanism.
    """
    
    def __init__(self, num_validators=4):
        self.validators = [f"validator_{i}" for i in range(num_validators)]
        self.num_validators = num_validators
        self.view = 0  # Current view number
        self.f = (num_validators - 1) // 3  # Max faulty nodes tolerated
        
    def _prepare_phase(self, block):
        """Simulate prepare phase - each validator validates the proposed block."""
        # In a real implementation, this would involve communication between nodes
        # Here we just simulate the result
        prepares = 0
        
        for i, validator in enumerate(self.validators):
            # Assume all honest validators agree
            if i < self.num_validators - self.f:
                prepares += 1
                
        # Need 2f + 1 prepares to proceed
        return prepares >= 2 * self.f + 1
    
    def _commit_phase(self, block):
        """Simulate commit phase where validators commit to the block."""
        # Similar to prepare, but for commit messages
        commits = 0
        
        for i, validator in enumerate(self.validators):
            # Assume all honest validators agree
            if i < self.num_validators - self.f:
                commits += 1
                
        # Need 2f + 1 commits to proceed
        return commits >= 2 * self.f + 1
    
    def find_consensus(self, block):
        """
        Find consensus on a block using PBFT protocol.
        In a simplified implementation:
        1. Pre-prepare: Leader proposes block
        2. Prepare: Validators validate & send prepare messages
        3. Commit: With enough prepares, validators commit
        4. Reply: With enough commits, block is added
        """
        # Add PBFT specific attributes
        block.view = self.view
        block.proposer = self.validators[self.view % self.num_validators]
        
        # Pre-prepare (already done - block is proposed)
        
        # Prepare phase
        prepare_success = self._prepare_phase(block)
        if not prepare_success:
            self.view += 1  # View change if prepare fails
            raise Exception("PBFT prepare phase failed")
            
        # Commit phase
        commit_success = self._commit_phase(block)
        if not commit_success:
            self.view += 1  # View change if commit fails
            raise Exception("PBFT commit phase failed")
            
        # Final hash calculation after consensus
        block.timestamp = time.time()  # Update timestamp
        block.consensus = "pbft"
        block.validators = self.validators.copy()
        block.hash = block.calculate_hash()
        
        return block