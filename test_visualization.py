#!/usr/bin/env python3
"""
Test visualization independently
"""

import warnings
import matplotlib
matplotlib.use('Agg')  # Set backend before importing pyplot
import matplotlib.pyplot as plt
import numpy as np

# Suppress protobuf warnings
warnings.filterwarnings("ignore", category=UserWarning, module="google.protobuf")

def test_basic_visualization():
    """Test basic matplotlib functionality"""
    print("🎨 Testing basic matplotlib...")
    
    try:
        fig, ax = plt.subplots(figsize=(10, 6))
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        
        ax.plot(x, y, label='sin(x)')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Test Plot')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('test_plot.png', dpi=150, bbox_inches='tight')
        plt.close(fig)
        
        print("✅ Basic matplotlib test passed")
        return True
        
    except Exception as e:
        print(f"❌ Basic matplotlib test failed: {e}")
        return False

def test_alphagenome_imports():
    """Test AlphaGenome imports"""
    print("📦 Testing AlphaGenome imports...")
    
    try:
        from alphagenome.models import dna_client
        print("✅ dna_client import successful")
        
        from alphagenome.data import genome
        print("✅ genome import successful")
        
        try:
            from alphagenome.visualization import plot_components
            print("✅ plot_components import successful")
            return True, True
        except ImportError as e:
            print(f"⚠️ plot_components import failed: {e}")
            return True, False
            
    except Exception as e:
        print(f"❌ AlphaGenome imports failed: {e}")
        return False, False

def test_alphagenome_connection():
    """Test AlphaGenome API connection"""
    print("🔗 Testing AlphaGenome connection...")
    
    try:
        from load_env_helper import get_api_key
        from alphagenome.models import dna_client
        
        api_key = get_api_key()
        if not api_key:
            print("❌ No API key found")
            return False
            
        model = dna_client.create(api_key)
        print("✅ Model client created")
        
        # Test a simple metadata call
        metadata = model.output_metadata(organism=dna_client.Organism.HOMO_SAPIENS)
        print("✅ Metadata fetch successful")
        
        return True
        
    except Exception as e:
        print(f"❌ AlphaGenome connection test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 AlphaGenome Visualization Test Suite")
    print("=" * 50)
    
    # Test 1: Basic matplotlib
    basic_viz_ok = test_basic_visualization()
    
    # Test 2: AlphaGenome imports
    imports_ok, viz_imports_ok = test_alphagenome_imports()
    
    # Test 3: API connection
    connection_ok = test_alphagenome_connection()
    
    print("\n" + "=" * 50)
    print("📋 Test Results:")
    print(f"   Basic Matplotlib: {'✅ PASS' if basic_viz_ok else '❌ FAIL'}")
    print(f"   AlphaGenome Core: {'✅ PASS' if imports_ok else '❌ FAIL'}")
    print(f"   Visualization Components: {'✅ PASS' if viz_imports_ok else '❌ FAIL'}")
    print(f"   API Connection: {'✅ PASS' if connection_ok else '❌ FAIL'}")
    
    if all([basic_viz_ok, imports_ok, connection_ok]):
        print("\n🎉 All tests passed! Streamlit visualization should work.")
    else:
        print("\n⚠️ Some tests failed. Check the issues above.")
    
    return all([basic_viz_ok, imports_ok, connection_ok])

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 