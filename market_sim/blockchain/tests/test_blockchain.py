import unittest
import time
from market_sim.blockchain.blockchain import Blockchain, Block
from market_sim.blockchain.consensus.pow import PowConsensus

class TestBlockchain(unittest.TestCase):
    def setUp(self):
        self.blockchain = Blockchain()
        
    def test_genesis_block(self):
        """Test if blockchain initializes with genesis block."""
        self.assertEqual(len(self.blockchain.chain), 1)
        self.assertEqual(self.blockchain.chain[0].index, 0)
        self.assertEqual(self.blockchain.chain[0].previous_hash, "0")
        
    def test_add_block(self):
        """Test adding a new block to the chain."""
        self.blockchain.add_transaction({"from": "Alice", "to": "Bob", "amount": 50})
        block = self.blockchain.mine_pending_transactions("miner1")
        
        self.assertEqual(len(self.blockchain.chain), 2)
        self.assertEqual(block.index, 1)
        self.assertEqual(len(block.transactions), 1)
        self.assertEqual(block.transactions[0]["amount"], 50)
        
    def test_blockchain_validity(self):
        """Test blockchain validation."""
        self.blockchain.add_transaction({"from": "Alice", "to": "Bob", "amount": 50})
        self.blockchain.mine_pending_transactions("miner1")
        
        # Chain should be valid
        self.assertTrue(self.blockchain.is_chain_valid())
        
        # Tamper with a block
        self.blockchain.chain[1].transactions[0]["amount"] = 100
        self.blockchain.chain[1].hash = self.blockchain.chain[1].calculate_hash()
        
        # Chain should be invalid due to broken link
        self.assertFalse(self.blockchain.is_chain_valid())
        
    def test_pow_consensus(self):
        """Test Proof of Work consensus mechanism."""
        pow_blockchain = Blockchain(consensus_mechanism=PowConsensus(difficulty=2))
        pow_blockchain.add_transaction({"from": "Alice", "to": "Bob", "amount": 50})
        block = pow_blockchain.mine_pending_transactions("miner1")
        
        # Block hash should start with difficulty number of zeros
        self.assertTrue(block.hash.startswith("00"))

if __name__ == "__main__":
    unittest.main()