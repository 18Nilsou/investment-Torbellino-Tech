import random
from typing import Any, Dict, List

class PoSConsensus:
    """Proof of Stake consensus mechanism."""
    
    def __init__(self):
        self.validators = {}  # address -> stake amount
        
    def add_validator(self, address: str, stake: float):
        """Add a validator with their stake."""
        self.validators[address] = stake
        
    def select_validator(self) -> str:
        """Select a validator based on stake."""
        total_stake = sum(self.validators.values())
        selection_point = random.uniform(0, total_stake)
        
        current_sum = 0
        for address, stake in self.validators.items():
            current_sum += stake
            if current_sum >= selection_point:
                return address
                
        # Fallback - should not reach here
        return list(self.validators.keys())[0]
        
    def find_consensus(self, block: Any) -> Any:
        """Validate block using proof of stake."""
        if not self.validators:
            return block  # No validators registered
            
        # Select validator and sign block
        validator = self.select_validator()
        block.validator = validator
        block.hash = block.calculate_hash()
        
        return block