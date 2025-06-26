#!/usr/bin/env python3
"""
Fix script for AlphaGenome protobuf compatibility issues
This script will reinstall the correct versions of protobuf and related packages
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command with error handling"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main fix function"""
    print("🧬 AlphaGenome Protobuf Compatibility Fix")
    print("=" * 50)
    
    # Check if we're in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    if not in_venv:
        print("⚠️  Warning: Not in a virtual environment")
        print("   It's recommended to use a virtual environment")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("Exiting...")
            return False
    
    print("🔍 Current Python environment:")
    print(f"   Python: {sys.executable}")
    print(f"   Virtual env: {'Yes' if in_venv else 'No'}")
    
    # Commands to fix the issue
    commands = [
        # Uninstall problematic packages
        ("pip uninstall -y protobuf grpcio grpcio-status", "Uninstalling existing protobuf packages"),
        
        # Install specific compatible versions
        ("pip install 'protobuf>=4.21.0,<5.0.0'", "Installing compatible protobuf"),
        ("pip install 'grpcio>=1.50.0'", "Installing compatible grpcio"),
        ("pip install 'grpcio-status>=1.50.0'", "Installing compatible grpcio-status"),
        
        # Reinstall AlphaGenome to ensure compatibility
        ("pip install --upgrade --force-reinstall alphagenome", "Reinstalling AlphaGenome"),
        
        # Install other requirements
        ("pip install -r requirements.txt", "Installing remaining requirements"),
    ]
    
    success_count = 0
    for cmd, description in commands:
        if run_command(cmd, description):
            success_count += 1
        else:
            print(f"⚠️  Failed: {description}")
    
    print("\n" + "=" * 50)
    if success_count == len(commands):
        print("🎉 All fixes applied successfully!")
        print("\n📋 Next steps:")
        print("1. Restart your Streamlit demo: python run_streamlit_demo.py")
        print("2. Test the API connection using the 'Test API Connection' button")
        print("3. Try running a prediction with a small genomic region first")
        
        # Test import
        print("\n🧪 Testing AlphaGenome import...")
        try:
            from alphagenome.models import dna_client
            print("✅ AlphaGenome import successful!")
        except Exception as e:
            print(f"❌ AlphaGenome import failed: {e}")
            
    else:
        print(f"⚠️  Some fixes failed ({success_count}/{len(commands)} succeeded)")
        print("You may need to manually resolve the remaining issues")
    
    return success_count == len(commands)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 