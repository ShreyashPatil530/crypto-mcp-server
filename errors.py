"""
Error handling module for the MCP server
Provides graceful error handling and logging
"""

import json
from datetime import datetime


class ErrorHandler:
    """Handles and logs errors gracefully"""
    
    def __init__(self, log_file='data/errors.log'):
        self.log_file = log_file
    
    def handle(self, exception, context="Unknown"):
        """
        Handle an exception gracefully
        Args:
            exception: The exception that occurred
            context (str): Context about where error occurred
        Returns: dict with error information
        """
        error_response = {
            'error': True,
            'message': str(exception),
            'context': context,
            'timestamp': datetime.now().isoformat(),
            'type': type(exception).__name__
        }
        
        self._log_error(error_response)
        self._print_error(error_response)
        
        return error_response
    
    def _log_error(self, error_info):
        """Log error to file"""
        try:
            import os
            os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
            
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(error_info) + '\n')
        except:
            pass  # Silently fail if logging fails
    
    def _print_error(self, error_info):
        """Print error to console"""
        print(f"\n❌ ERROR [{error_info['type']}]")
        print(f"   Context: {error_info['context']}")
        print(f"   Message: {error_info['message']}")
        print(f"   Time: {error_info['timestamp']}\n")
    
    def validate_symbol(self, symbol):
        """Validate if symbol is in correct format"""
        if not isinstance(symbol, str):
            raise ValueError("Symbol must be a string")
        if len(symbol) < 2 or len(symbol) > 10:
            raise ValueError("Symbol must be 2-10 characters")
        if not symbol.isupper():
            raise ValueError("Symbol must be uppercase")
        return True
    
    def validate_days(self, days):
        """Validate days parameter"""
        if not isinstance(days, int):
            raise ValueError("Days must be an integer")
        if days < 1 or days > 365:
            raise ValueError("Days must be between 1 and 365")
        return True