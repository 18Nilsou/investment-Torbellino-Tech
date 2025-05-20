from datetime import datetime

class Warrant:
    def __init__(self, strike_price, expiry_date, issuer, conversion_ratio, premium):
        self.strike_price = strike_price
        self.expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d")
        self.issuer = issuer
        self.conversion_ratio = conversion_ratio
        self.premium = premium

    def is_expired(self, current_date):
        return current_date > self.expiry_date

    def calculate_payoff(self, market_price):
        return max(0, (market_price - self.strike_price) * self.conversion_ratio) - self.premium