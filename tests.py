"""
Test cases for Cryptocurrency MCP Server
Tests all core functionality
"""

import unittest
import json
import os
from datetime import datetime
from api import CryptoAPI
from cache import CacheManager
from errors import ErrorHandler


class TestCryptoAPI(unittest.TestCase):
    """Test CryptoAPI class"""
    
    def setUp(self):
        self.api = CryptoAPI()
    
    def test_supported_symbols(self):
        """Test if API returns supported symbols"""
        symbols = self.api.get_supported_symbols()
        self.assertIn('BTC', symbols)
        self.assertIn('ETH', symbols)
        self.assertTrue(len(symbols) > 0)
        print("✓ Supported symbols test passed")
    
    def test_fetch_btc_price(self):
        """Test fetching Bitcoin price"""
        try:
            data = self.api.fetch_ticker('BTC')
            self.assertIn('price', data)
            self.assertIn('symbol', data)
            self.assertEqual(data['symbol'], 'BTC')
            self.assertGreater(data['price'], 0)
            print(f"✓ BTC price fetch test passed - Price: ${data['price']}")
        except Exception as e:
            self.fail(f"BTC fetch failed: {str(e)}")
    
    def test_fetch_eth_price(self):
        """Test fetching Ethereum price"""
        try:
            data = self.api.fetch_ticker('ETH')
            self.assertIn('price', data)
            self.assertEqual(data['symbol'], 'ETH')
            self.assertGreater(data['price'], 0)
            print(f"✓ ETH price fetch test passed - Price: ${data['price']}")
        except Exception as e:
            self.fail(f"ETH fetch failed: {str(e)}")
    
    def test_invalid_symbol(self):
        """Test error handling for invalid symbol"""
        try:
            self.api.fetch_ticker('INVALID123')
            self.fail("Should have raised an exception")
        except Exception as e:
            # Should raise an exception, this is correct behavior
            self.assertIn("not supported", str(e))
            print("✓ Invalid symbol test passed")
    
    def test_historical_data(self):
        """Test fetching historical data"""
        try:
            history = self.api.fetch_historical('BTC', days=5)
            self.assertIsInstance(history, list)
            self.assertGreater(len(history), 0)
            self.assertIn('date', history[0])
            self.assertIn('close', history[0])
            print(f"✓ Historical data test passed - Got {len(history)} data points")
        except Exception as e:
            self.fail(f"Historical data fetch failed: {str(e)}")
    
    def test_multiple_symbols(self):
        """Test fetching multiple symbols at once"""
        try:
            symbols = ['BTC', 'ETH', 'XRP']
            results = self.api.fetch_multiple_tickers(symbols)
            self.assertEqual(len(results), 3)
            self.assertIn('BTC', results)
            print("✓ Multiple symbols test passed")
        except Exception as e:
            self.fail(f"Multiple symbols fetch failed: {str(e)}")


class TestCacheManager(unittest.TestCase):
    """Test CacheManager class"""
    
    def setUp(self):
        self.cache = CacheManager('data/test_cache.json', ttl_minutes=60)
    
    def tearDown(self):
        """Clean up test cache file"""
        if os.path.exists('data/test_cache.json'):
            os.remove('data/test_cache.json')
    
    def test_save_and_get(self):
        """Test saving and retrieving cache"""
        test_data = {'price': 45000, 'symbol': 'BTC', 'timestamp': datetime.now().isoformat()}
        self.cache.save('BTC', test_data)
        
        retrieved = self.cache.get('BTC')
        self.assertEqual(retrieved['price'], 45000)
        print("✓ Cache save and get test passed")
    
    def test_cache_expiration(self):
        """Test cache expiration"""
        cache_short = CacheManager('data/test_cache2.json', ttl_minutes=0)
        test_data = {'price': 45000, 'timestamp': datetime.now().isoformat()}
        cache_short.save('BTC', test_data)
        
        # Should be expired
        retrieved = cache_short.get('BTC')
        self.assertIsNone(retrieved)
        print("✓ Cache expiration test passed")
    
    def test_cache_clear(self):
        """Test clearing cache"""
        self.cache.save('BTC', {'price': 45000, 'timestamp': datetime.now().isoformat()})
        self.cache.clear('BTC')
        
        retrieved = self.cache.get('BTC')
        self.assertIsNone(retrieved)
        print("✓ Cache clear test passed")
    
    def test_cache_file_creation(self):
        """Test if cache file is created"""
        test_data = {'price': 45000, 'timestamp': datetime.now().isoformat()}
        self.cache.save('BTC', test_data)
        
        self.assertTrue(os.path.exists('data/test_cache.json'))
        print("✓ Cache file creation test passed")


class TestErrorHandler(unittest.TestCase):
    """Test ErrorHandler class"""
    
    def setUp(self):
        self.error_handler = ErrorHandler('data/test_errors.log')
    
    def tearDown(self):
        """Clean up test files"""
        if os.path.exists('data/test_errors.log'):
            os.remove('data/test_errors.log')
    
    def test_error_handling(self):
        """Test error handling"""
        try:
            raise ValueError("Test error")
        except ValueError as e:
            result = self.error_handler.handle(e, "test context")
            self.assertTrue(result['error'])
            self.assertIn('Test error', result['message'])
            print("✓ Error handling test passed")
    
    def test_validate_symbol(self):
        """Test symbol validation"""
        self.assertTrue(self.error_handler.validate_symbol('BTC'))
        with self.assertRaises(ValueError):
            self.error_handler.validate_symbol('btc')  # lowercase
        print("✓ Symbol validation test passed")
    
    def test_validate_days(self):
        """Test days validation"""
        self.assertTrue(self.error_handler.validate_days(7))
        with self.assertRaises(ValueError):
            self.error_handler.validate_days(500)  # too many days
        print("✓ Days validation test passed")


def run_all_tests():
    """Run all test suites"""
    print("\n" + "="*50)
    print("🧪 Running Cryptocurrency MCP Server Tests")
    print("="*50 + "\n")
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestCryptoAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestCacheManager))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorHandler))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*50)
    if result.wasSuccessful():
        print(f"✅ All tests passed! ({result.testsRun} tests)")
    else:
        print(f"❌ Some tests failed ({len(result.failures)} failures, {len(result.errors)} errors)")
    print("="*50 + "\n")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_all_tests()
    exit(0 if success else 1)