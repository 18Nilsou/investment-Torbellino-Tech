import pytest
from datetime import datetime
from market_sim.blockchain.blockchain import Blockchain, Block
from market_sim.blockchain.consensus.pow import PowConsensus

class TestBlockchain:
    @pytest.fixture
    def blockchain(self):
        return Blockchain()
    
    @pytest.fixture
    def pow_blockchain(self):
        return Blockchain(consensus_mechanism=PowConsensus(difficulty=2))
    
    def test_genesis_block(self, blockchain):
        """Test genesis block creation."""
        assert len(blockchain.chain) == 1
        assert blockchain.chain[0].index == 0
        assert blockchain.chain[0].previous_hash == "0"
    
    def test_add_transaction(self, blockchain):
        """Test adding a transaction."""
        blockchain.add_transaction({"from": "Alice", "to": "Bob", "amount": 50})
        assert len(blockchain.pending_transactions) == 1
        assert blockchain.pending_transactions[0]["from"] == "Alice"
        
    def test_mine_pending_transactions(self, blockchain):
        """Test mining a block."""
        blockchain.add_transaction({"from": "Alice", "to": "Bob", "amount": 50})
        block = blockchain.mine_pending_transactions("miner1")
        
        assert len(blockchain.chain) == 2
        assert block.index == 1
        assert len(block.transactions) == 1
        assert blockchain.pending_transactions == []
        
    def test_chain_validation(self, blockchain):
        """Test chain validation."""
        blockchain.add_transaction({"from": "Alice", "to": "Bob", "amount": 50})
        blockchain.mine_pending_transactions("miner1")
        
        # Chain should be valid
        assert blockchain.is_chain_valid()
        
        # Tamper with a transaction
        blockchain.chain[1].transactions[0]["amount"] = 100
        blockchain.chain[1].hash = blockchain.chain[1].calculate_hash()
        
        # Chain should be invalid
        assert not blockchain.is_chain_valid()
        
    def test_pow_consensus(self, pow_blockchain):
        """Test Proof of Work consensus."""
        pow_blockchain.add_transaction({"from": "Alice", "to": "Bob", "amount": 50})
        block = pow_blockchain.mine_pending_transactions("miner1")
        
        # Block hash should start with two zeros (difficulty=2)
        assert block.hash.startswith("00")