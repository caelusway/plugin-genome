#!/usr/bin/env python3
"""
Basic AlphaGenome Example
This script demonstrates essential commands for interacting with the AlphaGenome API
based on the official documentation.
"""

import os
import sys

# Import our environment loader helper
from load_env_helper import get_api_key

def check_api_key():
    """Check if API key is set"""
    api_key = get_api_key()
    if not api_key:
        print("❌ ALPHA_GENOME_API_KEY environment variable not set")
        print("Please set your API key: export ALPHA_GENOME_API_KEY='your-api-key'")
        return False
    print("✅ API key found")
    return True

def basic_imports():
    """Import essential AlphaGenome modules"""
    try:
        print("📦 Importing AlphaGenome modules...")
        
        # Essential imports from documentation
        from alphagenome.data import genome
        from alphagenome.models import dna_client
        import numpy as np
        import pandas as pd
        
        print("✅ All imports successful")
        return True, (genome, dna_client, np, pd)
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False, None

def demonstrate_basic_usage():
    """Demonstrate basic AlphaGenome usage"""
    print("\n🧬 AlphaGenome Basic Usage Demo")
    print("=" * 40)
    
    # Check API key
    if not check_api_key():
        return False
    
    # Import modules
    success, modules = basic_imports()
    if not success:
        return False
    
    genome, dna_client, np, pd = modules
    
    print("\n📊 Available modules:")
    print(f"- genome: {genome}")
    print(f"- dna_client: {dna_client}")
    print(f"- numpy version: {np.__version__}")
    print(f"- pandas version: {pd.__version__}")
    
    print("\n🎯 Ready for AlphaGenome analysis!")
    print("You can now use the API to:")
    print("- Analyze DNA sequences up to 1 million base pairs")
    print("- Get predictions for gene expression, splicing patterns")
    print("- Analyze chromatin features and contact maps")
    print("- Perform variant effect predictions")
    
    return True

def main():
    """Main function"""
    print("🧬 AlphaGenome Basic Example")
    print("=" * 40)
    
    if demonstrate_basic_usage():
        print("\n✅ Example completed successfully!")
    else:
        print("\n❌ Example failed. Please check your setup.")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 