from market_sim.market.mechanisms import MarginAccount


class MarginSystem:
    """Enhanced margin trading system with risk management."""
    
    def __init__(self, initial_margin_requirement=0.5, maintenance_margin=0.25, 
                 liquidation_penalty=0.05):
        self.margin_accounts = {}
        self.initial_margin_requirement = initial_margin_requirement
        self.maintenance_margin = maintenance_margin
        self.liquidation_penalty = liquidation_penalty
        self.lending_pool = {}
        
    def create_margin_account(self, trader_id, initial_balance):
        """Create a new margin account."""
        self.margin_accounts[trader_id] = MarginAccount(initial_balance, 
                                                     self.initial_margin_requirement,
                                                     self.maintenance_margin,
                                                     self.liquidation_penalty)
        return self.margin_accounts[trader_id]
        
    def add_liquidity(self, provider_id, symbol, amount, interest_rate):
        """Add liquidity to the lending pool."""
        if symbol not in self.lending_pool:
            self.lending_pool[symbol] = []
            
        self.lending_pool[symbol].append({
            'provider': provider_id,
            'amount': amount,
            'interest_rate': interest_rate,
            'available': amount
        })
        
    def check_accounts(self, current_prices):
        """Check all margin accounts for liquidation conditions."""
        liquidations = []
        for trader_id, account in self.margin_accounts.items():
            if account.calculate_margin_call(current_prices):
                liquidation = self.liquidate_position(trader_id, current_prices)
                liquidations.append(liquidation)
        return liquidations