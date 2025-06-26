#!/usr/bin/env python3
"""
AlphaGenome Setup and Basic Usage
This script demonstrates how to set up and use AlphaGenome according to the official documentation.
"""

import sys
import subprocess
import os

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def install_alphagenome():
    """Install AlphaGenome package"""
    try:
        print("📦 Installing AlphaGenome...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-U", "alphagenome"], check=True)
        print("✅ AlphaGenome installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install AlphaGenome: {e}")
        return False

def test_import():
    """Test if AlphaGenome can be imported successfully"""
    try:
        print("🧪 Testing AlphaGenome import...")
        from alphagenome.data import genome
        from alphagenome.models import dna_client
        import numpy as np
        import pandas as pd
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🧬 AlphaGenome Setup Script")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install AlphaGenome
    if not install_alphagenome():
        return False
    
    # Test imports
    if not test_import():
        return False
    
    print("\n🎉 AlphaGenome setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Get your API key from the AlphaGenome platform")
    print("2. Set the ALPHA_GENOME_API_KEY environment variable")
    print("3. Run 'python basic_example.py' to test basic functionality")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 