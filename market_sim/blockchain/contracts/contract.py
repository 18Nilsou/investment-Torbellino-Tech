class SmartContract:
    """Base class for smart contracts."""
    
    def __init__(self, address: str, owner: str):
        self.address = address
        self.owner = owner
        self.state = {}
        
    def execute(self, method: str, params: dict, caller: str):
        """Execute a contract method."""
        if not hasattr(self, method):
            raise ValueError(f"Method {method} not found in contract")
            
        method_to_call = getattr(self, method)
        return method_to_call(params, caller)
        
    def get_state(self):
        """Return the current contract state."""
        return self.state