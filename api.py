"""
API module to fetch cryptocurrency data from exchanges using CCXT
No API keys needed - uses public endpoints
"""

import ccxt
from datetime import datetime, timedelta
import time


class CryptoAPI:
    """Handles all cryptocurrency API calls"""
    
    def __init__(self):
        # Using Binance - free, no API key needed
        self.exchange = ccxt.binance()
        self.symbols_map = {
            'BTC': 'BTC/USDT',
            'ETH': 'ETH/USDT',
            'XRP': 'XRP/USDT',
            'ADA': 'ADA/USDT',
            'SOL': 'SOL/USDT',
            'DOGE': 'DOGE/USDT',
            'MATIC': 'MATIC/USDT',
            'LINK': 'LINK/USDT',
            'LTC': 'LTC/USDT',
            'BCH': 'BCH/USDT',
            'DOT': 'DOT/USDT',
            'AVAX': 'AVAX/USDT',
            'ARB': 'ARB/USDT',
            'OP': 'OP/USDT',
            'SHIB': 'SHIB/USDT',
            'PEPE': 'PEPE/USDT',
            'NEAR': 'NEAR/USDT',
            'UNI': 'UNI/USDT'
        }
    
    def fetch_ticker(self, symbol):
        """
        Fetch current price and market data
        Args: symbol (str) - 'BTC', 'ETH', etc.
        Returns: dict with price, volume, 24h change
        """
        try:
            if symbol not in self.symbols_map:
                raise ValueError(f"Symbol {symbol} not supported")
            
            trading_pair = self.symbols_map[symbol]
            ticker = self.exchange.fetch_ticker(trading_pair)
            
            return {
                'symbol': symbol,
                'price': ticker['last'],
                'high_24h': ticker['high'],
                'low_24h': ticker['low'],
                'volume': ticker['quoteVolume'],
                'bid': ticker['bid'],
                'ask': ticker['ask'],
                'timestamp': datetime.now().isoformat(),
                'change_percent': ticker.get('percentage', 'N/A')
            }
        except Exception as e:
            raise Exception(f"Error fetching {symbol}: {str(e)}")
    
    def fetch_historical(self, symbol, days=7):
        """
        Fetch historical OHLCV data (Open, High, Low, Close, Volume)
        Args: symbol (str), days (int)
        Returns: list of candles with price history
        """
        try:
            if symbol not in self.symbols_map:
                raise ValueError(f"Symbol {symbol} not supported")
            
            trading_pair = self.symbols_map[symbol]
            
            # Fetch 1-day candles
            candles = self.exchange.fetch_ohlcv(
                trading_pair, 
                timeframe='1d', 
                limit=days
            )
            
            historical_data = []
            for candle in candles:
                timestamp, o, h, l, c, v = candle
                historical_data.append({
                    'date': datetime.fromtimestamp(timestamp/1000).isoformat(),
                    'open': o,
                    'high': h,
                    'low': l,
                    'close': c,
                    'volume': v
                })
            
            return historical_data
        except Exception as e:
            raise Exception(f"Error fetching historical data for {symbol}: {str(e)}")
    
    def get_supported_symbols(self):
        """Return list of supported cryptocurrencies"""
        return list(self.symbols_map.keys())
    
    def fetch_multiple_tickers(self, symbols):
        """
        Fetch data for multiple cryptocurrencies at once
        Args: symbols (list) - ['BTC', 'ETH', 'XRP']
        Returns: dict with all ticker data
        """
        results = {}
        for symbol in symbols:
            try:
                results[symbol] = self.fetch_ticker(symbol)
            except Exception as e:
                results[symbol] = {'error': str(e)}
        return results