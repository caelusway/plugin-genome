#!/usr/bin/env python3
"""
Environment Variable Helper
Loads environment variables from .env files with fallback methods
"""

import os
import sys

def get_api_key():
    """
    Get AlphaGenome API key from environment variables
    Tries multiple methods to load from .env files
    """
    
    # Method 1: Check if already in environment
    api_key = os.getenv('ALPHA_GENOME_API_KEY')
    if api_key:
        return api_key
    
    # Method 2: Try python-dotenv
    try:
        from dotenv import load_dotenv
        
        # Try loading from current directory
        if os.path.exists('.env'):
            load_dotenv('.env')
            api_key = os.getenv('ALPHA_GENOME_API_KEY')
            if api_key:
                return api_key
        
        # Try loading from parent directory
        if os.path.exists('../.env'):
            load_dotenv('../.env')
            api_key = os.getenv('ALPHA_GENOME_API_KEY')
            if api_key:
                return api_key
                
    except ImportError:
        print("python-dotenv not available, trying manual parsing...")
    
    # Method 3: Manual .env file parsing
    env_files = ['.env', '../.env']
    
    for env_file in env_files:
        if os.path.exists(env_file):
            try:
                with open(env_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            
                            if key == 'ALPHA_GENOME_API_KEY' and value:
                                os.environ[key] = value
                                return value
            except Exception as e:
                print(f"Error reading {env_file}: {e}")
    
    # Method 4: Check common environment file locations
    home_env = os.path.expanduser('~/.env')
    if os.path.exists(home_env):
        try:
            with open(home_env, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        
                        if key == 'ALPHA_GENOME_API_KEY' and value:
                            os.environ[key] = value
                            return value
        except Exception as e:
            print(f"Error reading {home_env}: {e}")
    
    return None

def load_env_variables():
    """
    Load all environment variables from .env files
    """
    try:
        from dotenv import load_dotenv
        
        # Try loading from current directory first
        if os.path.exists('.env'):
            load_dotenv('.env')
            return True
        
        # Try loading from parent directory
        if os.path.exists('../.env'):
            load_dotenv('../.env')
            return True
            
    except ImportError:
        pass
    
    # Manual loading as fallback
    env_files = ['.env', '../.env', os.path.expanduser('~/.env')]
    
    for env_file in env_files:
        if os.path.exists(env_file):
            try:
                with open(env_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            
                            if key and value:
                                os.environ[key] = value
                return True
            except Exception as e:
                print(f"Error reading {env_file}: {e}")
    
    return False

def check_environment():
    """
    Check if the environment is properly configured
    """
    api_key = get_api_key()
    
    if not api_key:
        print("❌ ALPHA_GENOME_API_KEY not found")
        print("Please set your API key in one of these ways:")
        print("1. Create a .env file with: ALPHA_GENOME_API_KEY=your-key")
        print("2. Export it: export ALPHA_GENOME_API_KEY=your-key")
        print("3. Get your API key from: https://deepmind.google.com/science/alphagenome")
        return False
    
    print("✅ ALPHA_GENOME_API_KEY found")
    return True

if __name__ == "__main__":
    print("🔧 Environment Helper Test")
    print("=" * 30)
    
    # Test environment loading
    load_env_variables()
    
    # Check API key
    api_key = get_api_key()
    if api_key:
        print(f"✅ API Key found: {api_key[:10]}...")
    else:
        print("❌ API Key not found")
    
    # Full environment check
    check_environment() 