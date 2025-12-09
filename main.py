"""
Main entry point for Cryptocurrency MCP Server
Starts the server and handles real-time crypto data requests
"""

import json
from datetime import datetime
from api import CryptoAPI
from cache import CacheManager
from errors import ErrorHandler


class MCPServer:
    """Main MCP Server for cryptocurrency data"""
    
    def __init__(self):
        self.api = CryptoAPI()
        self.cache = CacheManager()
        self.error_handler = ErrorHandler()
    
    def get_current_price(self, symbol):
        """
        Get current price of cryptocurrency
        Args: symbol (str) - Like 'BTC', 'ETH', 'XRP'
        Returns: dict with price and timestamp
        """
        try:
            # Check cache first
            cached = self.cache.get(symbol)
            if cached:
                print(f"✓ Got {symbol} from cache")
                return cached
            
            # If not in cache, fetch from API
            price_data = self.api.fetch_ticker(symbol)
            
            # Save to cache
            self.cache.save(symbol, price_data)
            print(f"✓ Fetched {symbol} from exchange and cached")
            return price_data
            
        except Exception as e:
            return self.error_handler.handle(e, symbol)
    
    def get_multiple_prices(self, symbols):
        """
        Get prices for multiple cryptocurrencies
        Args: symbols (list) - ['BTC', 'ETH', 'XRP']
        Returns: dict with all prices
        """
        results = {}
        for symbol in symbols:
            results[symbol] = self.get_current_price(symbol)
        return results
    
    def get_historical_data(self, symbol, days=7):
        """
        Get historical price data
        Args: symbol (str), days (int)
        Returns: list of historical prices
        """
        try:
            data = self.api.fetch_historical(symbol, days)
            print(f"✓ Got {days} days of historical data for {symbol}")
            return data
        except Exception as e:
            return self.error_handler.handle(e, f"{symbol} (historical)")
    
    def start(self):
        """Start the MCP server"""
        print("=" * 50)
        print("🚀 Cryptocurrency MCP Server Started")
        print("=" * 50)
        
        # Example usage
        print("\n📊 Fetching live prices...")
        btc = self.get_current_price('BTC')
        eth = self.get_current_price('ETH')
        
        print(f"\nBTC: ${btc.get('price', 'N/A')}")
        print(f"ETH: ${eth.get('price', 'N/A')}")
        
        print("\n📈 Fetching historical data (last 5 days)...")
        history = self.get_historical_data('BTC', days=5)
        print(f"Historical data points: {len(history)}")
        
        print("\n✅ Server running successfully!")


if __name__ == "__main__":
    server = MCPServer()
    server.start()