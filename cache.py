"""
Cache module to store cryptocurrency data locally
Reduces API calls and improves performance
"""

import json
import os
from datetime import datetime, timedelta


class CacheManager:
    """Manages caching of cryptocurrency data"""
    
    def __init__(self, cache_file='data/cache.json', ttl_minutes=5):
        """
        Initialize cache manager
        Args:
            cache_file (str): Path to cache file
            ttl_minutes (int): Time to live for cached data (5 min default)
        """
        self.cache_file = cache_file
        self.ttl_minutes = ttl_minutes
        self.cache_data = self._load_cache()
    
    def _ensure_data_dir(self):
        """Create data directory if it doesn't exist"""
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
    
    def _load_cache(self):
        """Load cache from JSON file"""
        self._ensure_data_dir()
        
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_cache(self):
        """Save cache to JSON file"""
        self._ensure_data_dir()
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache_data, f, indent=2)
    
    def _is_expired(self, timestamp_str):
        """Check if cached data has expired"""
        try:
            cached_time = datetime.fromisoformat(timestamp_str)
            expiry_time = cached_time + timedelta(minutes=self.ttl_minutes)
            return datetime.now() > expiry_time
        except:
            return True
    
    def get(self, symbol):
        """
        Get cached data for a symbol
        Args: symbol (str) - 'BTC', 'ETH', etc.
        Returns: dict if valid cache exists, None if expired or missing
        """
        if symbol not in self.cache_data:
            return None
        
        cached_entry = self.cache_data[symbol]
        
        if self._is_expired(cached_entry.get('timestamp', '')):
            # Remove expired entry
            del self.cache_data[symbol]
            self._save_cache()
            return None
        
        return cached_entry
    
    def save(self, symbol, data):
        """
        Save data to cache
        Args: symbol (str), data (dict)
        """
        self.cache_data[symbol] = data
        self._save_cache()
    
    def clear(self, symbol=None):
        """
        Clear cache for specific symbol or all
        Args: symbol (str) - None to clear all
        """
        if symbol:
            if symbol in self.cache_data:
                del self.cache_data[symbol]
        else:
            self.cache_data = {}
        
        self._save_cache()
    
    def get_cache_info(self):
        """Get information about cached data"""
        info = {
            'file': self.cache_file,
            'ttl_minutes': self.ttl_minutes,
            'cached_symbols': list(self.cache_data.keys()),
            'total_entries': len(self.cache_data)
        }
        return info