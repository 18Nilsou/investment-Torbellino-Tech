import pytest
import time
from market_sim.blockchain.blockchain import Blockchain
from market_sim.blockchain.consensus.pow import PowConsensus

class TestBlockchainPerformance:
    @pytest.mark.performance
    def test_blockchain_transaction_throughput(self):
        """Test blockchain transaction throughput."""
        blockchain = Blockchain(consensus_mechanism=PowConsensus(difficulty=4))
        
        # Prepare transactions
        num_transactions = 100
        transactions = [
            {"from": f"user{i}", "to": f"user{i+1}", "amount": 100}
            for i in range(num_transactions)
        ]
        
        # Measure time to add transactions
        start_time = time.time()
        for tx in transactions:
            blockchain.add_transaction(tx)
        add_time = time.time() - start_time
        
        # Measure time to mine a block
        start_time = time.time()
        blockchain.mine_pending_transactions("miner")
        mine_time = time.time() - start_time
        
        # Print performance metrics
        print(f"Added {num_transactions} transactions in {add_time:.4f}s ({num_transactions/add_time:.2f} tx/s)")
        print(f"Mined block with {num_transactions} transactions in {mine_time:.4f}s")
        
        # Check that all transactions were processed
        assert len(blockchain.pending_transactions) == 0
        assert len(blockchain.chain[1].transactions) == num_transactions