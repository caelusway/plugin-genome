#!/usr/bin/env python3
"""
Environment Variable Loader Helper
Loads environment variables from .env file if available
"""

import os
import sys

def load_env():
    """Load environment variables from .env file if it exists"""
    try:
        # Try to import python-dotenv
        from dotenv import load_dotenv
        
        # Look for .env file in current directory and parent directories
        env_files = ['.env', '../.env', '../../.env']
        
        for env_file in env_files:
            if os.path.exists(env_file):
                load_dotenv(env_file)
                print(f"✅ Loaded environment variables from {env_file}")
                return True
        
        # If no .env file found, try loading from current directory
        load_dotenv()
        return True
        
    except ImportError:
        # python-dotenv not installed, try manual loading
        return load_env_manual()

def load_env_manual():
    """Manually load .env file if python-dotenv is not available"""
    env_files = ['.env', '../.env', '../../.env']
    
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
                            os.environ[key] = value
                print(f"✅ Manually loaded environment variables from {env_file}")
                return True
            except Exception as e:
                print(f"⚠️ Error loading {env_file}: {e}")
    
    return False

def get_api_key():
    """Get API key from environment, loading .env if necessary"""
    # First try to load from .env
    load_env()
    
    # Now get the API key
    api_key = os.getenv('ALPHA_GENOME_API_KEY')
    
    if not api_key:
        print("❌ ALPHA_GENOME_API_KEY not found")
        print("📝 Options to set your API key:")
        print("1. Create a .env file with: ALPHA_GENOME_API_KEY='your-api-key'")
        print("2. Export in terminal: export ALPHA_GENOME_API_KEY='your-api-key'")
        print("3. Get your API key from: https://deepmind.google.com/science/alphagenome")
        return None
    
    print("✅ API key loaded successfully")
    return api_key

if __name__ == "__main__":
    # Test the loader
    api_key = get_api_key()
    if api_key:
        print(f"🔑 API key found: {api_key[:10]}...")
    else:
        print("❌ No API key found") 