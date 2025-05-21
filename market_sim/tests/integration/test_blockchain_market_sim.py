import pytest
from datetime import datetime, timedelta
from core.models.base import Asset, Order
from market.agents.base_agent import BaseAgent
from market_sim.simulation.engine.simulation_engine import MarketSimulation
from market_sim.blockchain.ethereum.ethereum_network import EthereumNetwork

class SimpleAgent(BaseAgent):
    """Simple agent for testing."""
    def __init__(self, agent_id, cash=10000):
        super().__init__(agent_id, cash)
        
    def on_time_update(self, current_time):
        # Every 3 time steps, place a buy order
        if hasattr(self, 'last_time') and (current_time - self.last_time).total_seconds() > 3:
            self.place_order(
                Order(
                    symbol="TEST",
                    side="buy",
                    order_type="limit",
                    quantity=1,
                    price=100
                )
            )
        self.last_time = current_time

class TestBlockchainMarketSim:
    @pytest.fixture
    def simulation(self):
        # Create simulation
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=10)
        time_step = timedelta(seconds=1)
        
        sim = MarketSimulation(start_time, end_time, time_step)
        
        # Add test asset
        test_asset = Asset("TEST", "Test Asset", 100.0)
        sim.add_asset(test_asset)
        
        # Add test exchange
        sim.add_exchange("TEST")
        
        # Add test agents
        buyer = SimpleAgent("buyer")
        seller = SimpleAgent("seller")
        sim.add_agent(buyer)
        sim.add_agent(seller)
        
        # Initialize
        sim.initialize()
        
        return sim
    
    def test_blockchain_integration(self, simulation):
        """Test blockchain integration with market simulation."""
        # Verify blockchain components are initialized
        assert simulation.blockchain_integration is not None
        assert simulation.blockchain_integration.blockchain is not None
        assert simulation.blockchain_integration.ethereum is not None
        
        # Verify agent accounts are created
        assert len(simulation.blockchain_integration.ethereum.accounts) >= 2
        
        # Run a short simulation
        simulation.end_time = simulation.start_time + timedelta(seconds=10)
        results = simulation.run()
        
        # Check trades were recorded on blockchain
        total_trades = len(results['trades'])
        assert len(simulation.blockchain_integration.trade_history) == total_trades
        
        # Check blocks were mined (if any trades occurred)
        if total_trades > 0:
            assert len(simulation.blockchain_integration.blockchain.chain) > 1
        
        # Verify trade contracts were deployed
        assert "TEST" in simulation.blockchain_integration.trade_contracts
        
    def test_trade_recording(self, simulation):
        """Test that trades are properly recorded on the blockchain."""
        # Create and process a test order
        order = Order(
            symbol="TEST",
            side="buy",
            order_type="limit",
            quantity=1,
            price=100
        )
        
        # Add a matching order from opposite side
        matching_order = Order(
            symbol="TEST",
            side="sell",
            order_type="limit",
            quantity=1,
            price=100
        )
        
        # Process orders
        simulation.process_order(matching_order)  # Add sell order to book
        trades = simulation.process_order(order)  # Should match with sell order
        
        # Verify trade was recorded on blockchain
        if trades:
            assert len(simulation.blockchain_integration.trade_history) > 0
            recorded_trade = simulation.blockchain_integration.trade_history[0]
            assert recorded_trade["symbol"] == "TEST"
            assert recorded_trade["price"] == 100