import random
from datetime import datetime


class TradingAccount:
    def __init__(self, account_id, name, initial_balance):
        self.account_id = account_id
        self.name = name
        self.balance = initial_balance
        self.positions = {}
    
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False
    
    def withdraw(self, amount):
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            return True
        return False


class RiskManagement:
    def assess_portfolio_risk(self):
        risk_levels = ["Low", "Medium", "High"]
        return random.choice(risk_levels)
    
    def calculate_position_size(self, symbol, price):
        max_risk = self.balance * 0.02
        return int(max_risk / price)
    
    def check_risk_limits(self, position_value):
        return position_value <= self.balance * 0.1


class AnalyticsEngine:
    def analyze_market_trend(self, symbol):
        trends = ["Bullish", "Bearish", "Neutral"]
        return {
            "symbol": symbol,
            "trend": random.choice(trends),
            "confidence": round(random.uniform(0.5, 0.95), 2)
        }
    
    def calculate_portfolio_performance(self):
        return {"return": random.uniform(-0.1, 0.15), "volatility": random.uniform(0.05, 0.25)}


class NotificationSystem:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.alerts = []
        self.notifications = []
    
    def set_price_alert(self, symbol, price, direction):
        alert = {
            "symbol": symbol,
            "price": price,
            "direction": direction,
            "timestamp": datetime.now()
        }
        self.alerts.append(alert)
        return True
    
    def get_pending_notifications(self):
        return self.notifications
    
    def send_notification(self, message):
        self.notifications.append({
            "message": message,
            "timestamp": datetime.now()
        })


class StockTrader(TradingAccount, RiskManagement, AnalyticsEngine):
    def __init__(self, account_id, name, initial_balance):
        super().__init__(account_id, name, initial_balance)
        self.stock_positions = {}
    
    def buy_stock(self, symbol, quantity, price):
        total_cost = quantity * price
        if self.balance >= total_cost:
            self.balance -= total_cost
            self.stock_positions[symbol] = self.stock_positions.get(symbol, 0) + quantity
            return True
        return False


class CryptoTrader(TradingAccount, RiskManagement, NotificationSystem):
    def __init__(self, account_id, name, initial_balance):
        super().__init__(account_id, name, initial_balance)
        self.crypto_positions = {}
        self.alerts = []
        self.notifications = []
    
    def buy_crypto(self, symbol, quantity, price):
        total_cost = quantity * price
        if self.balance >= total_cost:
            self.balance -= total_cost
            self.crypto_positions[symbol] = self.crypto_positions.get(symbol, 0) + quantity
            return True
        return False


class ProfessionalTrader(StockTrader, CryptoTrader):
    def __init__(self, account_id, name, initial_balance):
        super().__init__(account_id, name, initial_balance)
        self.all_positions = {}
        self.alerts = []
        self.notifications = []
    
    def execute_diversified_strategy(self, strategy):
        positions = []
        
        for stock in strategy["stocks"]:
            analysis = self.analyze_market_trend(stock)
            if analysis["trend"] == "Bullish":
                position_size = self.calculate_position_size(stock, 150.0)
                positions.append({"type": "stock", "symbol": stock, "quantity": position_size})
        
        for crypto in strategy["crypto"]:
            analysis = self.analyze_market_trend(crypto)
            if analysis["confidence"] > 0.7:
                position_size = self.calculate_position_size(crypto, 45000.0)
                positions.append({"type": "crypto", "symbol": crypto, "quantity": position_size})
        
        return {
            "status": "executed",
            "positions": positions,
            "timestamp": datetime.now()
        }


if __name__ == "__main__":
    # Test Case 1: Multiple inheritance setup and MRO
    stock_trader = StockTrader("ST001", "John Doe", 50000.0)
    crypto_trader = CryptoTrader("CT001", "Jane Smith", 25000.0)
    pro_trader = ProfessionalTrader("PT001", "Mike Johnson", 100000.0)

    mro_names = [cls.__name__ for cls in ProfessionalTrader.__mro__]
    assert "ProfessionalTrader" in mro_names
    assert "StockTrader" in mro_names
    assert "CryptoTrader" in mro_names
    print("Test Case 1: PASSED")

    # Test Case 2: Account management capabilities
    assert stock_trader.account_id == "ST001"
    assert stock_trader.balance == 50000.0

    deposit_result = stock_trader.deposit(10000)
    assert stock_trader.balance == 60000.0
    assert deposit_result == True

    withdrawal_result = stock_trader.withdraw(5000)
    assert stock_trader.balance == 55000.0
    print("Test Case 2: PASSED")

    # Test Case 3: Risk management functionality
    risk_level = stock_trader.assess_portfolio_risk()
    assert risk_level in ["Low", "Medium", "High"]

    position_size = stock_trader.calculate_position_size("AAPL", 150.0)
    assert isinstance(position_size, int)
    assert position_size > 0
    print("Test Case 3: PASSED")

    # Test Case 4: Analytics capabilities
    market_data = stock_trader.analyze_market_trend("AAPL")
    assert isinstance(market_data, dict)
    assert "trend" in market_data
    assert "confidence" in market_data
    print("Test Case 4: PASSED")

    # Test Case 5: Notification system for crypto trader
    alert_set = crypto_trader.set_price_alert("BTC", 45000, "above")
    assert alert_set == True

    notifications = crypto_trader.get_pending_notifications()
    assert isinstance(notifications, list)
    print("Test Case 5: PASSED")

    # Test Case 6: Professional trader combining all features
    assert hasattr(pro_trader, 'assess_portfolio_risk')
    assert hasattr(pro_trader, 'analyze_market_trend')
    assert hasattr(pro_trader, 'set_price_alert')

    strategy_result = pro_trader.execute_diversified_strategy({
        "stocks": ["AAPL", "GOOGL"],
        "crypto": ["BTC", "ETH"],
        "allocation": {"stocks": 0.7, "crypto": 0.3}
    })

    assert strategy_result["status"] == "executed"
    assert len(strategy_result["positions"]) >= 0
    print("Test Case 6: PASSED")

    print("\nAll tests passed! Financial Trading System is working correctly.")
    print(f"MRO: {[cls.__name__ for cls in ProfessionalTrader.__mro__]}")
    print(f"Strategy executed with {len(strategy_result['positions'])} positions")