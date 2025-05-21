from typing import Dict, List, Any
import hashlib
import time
import secrets

class Account:
    """Ethereum account representation."""
    
    def __init__(self, private_key=None):
        self.private_key = private_key or secrets.token_hex(32)
        self.address = self._derive_address()
        self.balance = 0
        
    def _derive_address(self):
        """Derive an Ethereum-like address from the private key."""
        return hashlib.sha256(self.private_key.encode()).hexdigest()[-40:]
    
    def sign_message(self, message):
        """Simulate signing a message with the private key."""
        signature = hashlib.sha256((self.private_key + message).encode()).hexdigest()
        return signature

class EthereumNetwork:
    """Simplified Ethereum network simulation."""
    
    def __init__(self):
        self.accounts = {}
        self.contracts = {}
        self.transactions = []
        self.gas_price = 1
        self.chain = []
        
    def create_account(self) -> Account:
        """Create a new Ethereum account."""
        account = Account()
        self.accounts[account.address] = account
        return account
        
    def get_balance(self, address: str) -> float:
        """Get account balance."""
        if address in self.accounts:
            return self.accounts[address].balance
        return 0
        
    def transfer(self, from_address: str, to_address: str, amount: float) -> bool:
        """Transfer ETH between accounts."""
        if from_address not in self.accounts or to_address not in self.accounts:
            return False
            
        sender = self.accounts[from_address]
        if sender.balance < amount:
            return False
            
        sender.balance -= amount
        self.accounts[to_address].balance += amount
        
        tx = {
            "hash": secrets.token_hex(32),
            "from": from_address,
            "to": to_address,
            "value": amount,
            "timestamp": time.time()
        }
        self.transactions.append(tx)
        
        return True
        
    def deploy_contract(self, creator_address: str, contract_code: str, gas_limit: int = 1000000) -> str:
        """Deploy a contract to the network."""
        if creator_address not in self.accounts:
            return None
            
        gas_cost = len(contract_code) * self.gas_price
        if gas_cost > gas_limit or self.accounts[creator_address].balance < gas_cost:
            return None
            
        # Generate contract address
        contract_address = hashlib.sha256(
            (creator_address + str(time.time())).encode()
        ).hexdigest()[-40:]
        
        self.contracts[contract_address] = {
            "code": contract_code,
            "creator": creator_address,
            "created_at": time.time()
        }
        
        # Deduct gas cost
        self.accounts[creator_address].balance -= gas_cost
        
        return contract_address
        
    def call_contract(self, caller_address: str, contract_address: str, method: str, params: Dict) -> Any:
        """Call a contract method (read-only)."""
        if contract_address not in self.contracts:
            return None
            
        # In a real implementation, this would execute the contract code
        # Here we just record the call
        call = {
            "caller": caller_address,
            "contract": contract_address,
            "method": method,
            "params": params,
            "timestamp": time.time()
        }
        
        return {"status": "success", "call": call}