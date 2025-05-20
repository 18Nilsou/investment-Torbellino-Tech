class MarginAccount:
    def __init__(self, initial_balance, leverage_ratio):
        self.balance = initial_balance
        self.leverage_ratio = leverage_ratio
        self.borrowed_funds = 0

    def borrow(self, amount):
        self.borrowed_funds += amount
        self.balance += amount

    def calculate_margin_call(self, market_value):
        equity = self.balance - self.borrowed_funds
        margin_ratio = equity / market_value
        return margin_ratio < 0.25  # Example: Margin call if equity < 25% of market value

    def liquidate(self):
        self.balance = 0
        self.borrowed_funds = 0