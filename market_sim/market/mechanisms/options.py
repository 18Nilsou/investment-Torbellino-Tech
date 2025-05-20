from datetime import datetime

class Option:
    def __init__(self, strike_price, expiry_date, option_type, premium):
        self.strike_price = strike_price
        self.expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d")
        self.option_type = option_type.lower()
        self.premium = premium

    def is_expired(self, current_date):
        return current_date > self.expiry_date

    def calculate_payoff(self, market_price):
        if self.option_type == "call":
            return max(0, market_price - self.strike_price) - self.premium
        elif self.option_type == "put":
            return max(0, self.strike_price - market_price) - self.premium
        else:
            raise ValueError("Invalid option type. Must be 'call' or 'put'.")