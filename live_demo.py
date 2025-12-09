"""
Live Demo - Shows ALL cryptocurrencies with real-time data
Run this to see all crypto prices at once (LIVE, not cached)
"""

import json
from datetime import datetime
from api import CryptoAPI
from cache import CacheManager


class LiveCryptoDemo:
    """Live cryptocurrency data demonstration"""
    
    def __init__(self):
        self.api = CryptoAPI()
        self.cache = CacheManager()
    
    def show_all_live_prices(self):
        """Fetch and display ALL cryptocurrency prices LIVE"""
        print("\n" + "="*70)
        print("🔴 LIVE CRYPTOCURRENCY DATA - REAL-TIME PRICES")
        print("="*70)
        print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70 + "\n")
        
        symbols = self.api.get_supported_symbols()
        print(f"📊 Fetching LIVE prices for {len(symbols)} cryptocurrencies...\n")
        
        # Clear cache to force fresh data
        self.cache.clear()
        
        all_data = {}
        
        for i, symbol in enumerate(symbols, 1):
            try:
                print(f"[{i}/{len(symbols)}] Fetching {symbol}...", end=" ", flush=True)
                data = self.api.fetch_ticker(symbol)
                all_data[symbol] = data
                
                price = data['price']
                change = data['change_percent']
                arrow = "📈" if change > 0 else "📉" if change < 0 else "➡️"
                
                print(f"✓ ${price:,.2f} {arrow} ({change:+.2f}%)")
                
            except Exception as e:
                print(f"❌ Error: {str(e)}")
        
        print("\n" + "="*70)
        print("📋 SUMMARY TABLE - ALL CRYPTOCURRENCIES")
        print("="*70)
        print(f"{'Symbol':<10} {'Price (USDT)':<18} {'24h High':<18} {'24h Low':<18} {'Change %':<12}")
        print("-"*70)
        
        for symbol, data in all_data.items():
            if 'error' not in data:
                symbol_str = f"{data['symbol']:<10}"
                price_str = f"${data['price']:>15,.2f}"
                high_str = f"${data['high_24h']:>15,.2f}"
                low_str = f"${data['low_24h']:>15,.2f}"
                change_str = f"{data['change_percent']:>10.2f}%"
                
                print(f"{symbol_str} {price_str} {high_str} {low_str} {change_str}")
        
        print("="*70 + "\n")
        
        # Save to JSON file
        self._save_live_data(all_data)
        
        return all_data
    
    def show_detailed_data(self, symbol):
        """Show detailed data for a specific cryptocurrency"""
        print("\n" + "="*70)
        print(f"📊 DETAILED DATA - {symbol}")
        print("="*70 + "\n")
        
        try:
            # Clear cache for fresh data
            self.cache.clear(symbol)
            
            data = self.api.fetch_ticker(symbol)
            
            print(f"Symbol:           {data['symbol']}")
            print(f"Current Price:    ${data['price']:,.2f}")
            print(f"24h High:         ${data['high_24h']:,.2f}")
            print(f"24h Low:          ${data['low_24h']:,.2f}")
            print(f"24h Change:       {data['change_percent']:+.2f}%")
            print(f"Bid Price:        ${data['bid']:,.2f}")
            print(f"Ask Price:        ${data['ask']:,.2f}")
            print(f"Volume (24h):     ${data['volume']:,.0f}")
            print(f"Updated:          {data['timestamp']}")
            
            print("\n" + "="*70)
            print("📈 HISTORICAL DATA (Last 7 Days)")
            print("="*70 + "\n")
            print(f"{'Date':<25} {'Open':<15} {'High':<15} {'Low':<15} {'Close':<15}")
            print("-"*70)
            
            history = self.api.fetch_historical(symbol, days=7)
            
            for candle in history:
                date = candle['date'][:10]  # Just the date part
                open_price = f"${candle['open']:,.2f}"
                high = f"${candle['high']:,.2f}"
                low = f"${candle['low']:,.2f}"
                close = f"${candle['close']:,.2f}"
                
                print(f"{date:<25} {open_price:<15} {high:<15} {low:<15} {close:<15}")
            
            print("\n" + "="*70 + "\n")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}\n")
    
    def show_top_gainers(self, all_data, top_n=5):
        """Show top gaining cryptocurrencies"""
        print("\n" + "="*70)
        print(f"🚀 TOP {top_n} GAINERS (24h)")
        print("="*70 + "\n")
        
        sorted_data = sorted(
            all_data.items(),
            key=lambda x: x[1].get('change_percent', 0),
            reverse=True
        )
        
        for i, (symbol, data) in enumerate(sorted_data[:top_n], 1):
            if 'error' not in data:
                change = data['change_percent']
                price = data['price']
                print(f"{i}. {symbol:<8} ${price:>12,.2f}  📈 +{change:.2f}%")
        
        print("\n")
    
    def show_top_losers(self, all_data, top_n=5):
        """Show top losing cryptocurrencies"""
        print("\n" + "="*70)
        print(f"📉 TOP {top_n} LOSERS (24h)")
        print("="*70 + "\n")
        
        sorted_data = sorted(
            all_data.items(),
            key=lambda x: x[1].get('change_percent', 0)
        )
        
        for i, (symbol, data) in enumerate(sorted_data[:top_n], 1):
            if 'error' not in data:
                change = data['change_percent']
                price = data['price']
                print(f"{i}. {symbol:<8} ${price:>12,.2f}  📉 {change:.2f}%")
        
        print("\n")
    
    def _save_live_data(self, data):
        """Save live data to JSON file"""
        output_file = 'data/live_prices.json'
        try:
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"💾 Live data saved to: {output_file}")
        except Exception as e:
            print(f"⚠️  Could not save file: {str(e)}")


def main():
    """Main demo function"""
    demo = LiveCryptoDemo()
    
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█" + "  CRYPTOCURRENCY MCP SERVER - LIVE DATA DEMO".center(68) + "█")
    print("█" + " "*68 + "█")
    print("█"*70)
    
    # Show all live prices
    all_data = demo.show_all_live_prices()
    
    # Show top gainers and losers
    demo.show_top_gainers(all_data, top_n=5)
    demo.show_top_losers(all_data, top_n=5)
    
    # Show detailed data for specific symbols
    print("\n" + "="*70)
    print("📌 DETAILED VIEW - BTC")
    print("="*70)
    demo.show_detailed_data('BTC')
    
    print("="*70)
    print("📌 DETAILED VIEW - ETH")
    print("="*70)
    demo.show_detailed_data('ETH')
    
    print("\n✅ Live demo completed! Check 'data/live_prices.json' for full data.")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()