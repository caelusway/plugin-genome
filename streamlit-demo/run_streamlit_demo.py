#!/usr/bin/env python3
"""
Launch script for the AlphaGenome Streamlit demo
"""

import subprocess
import sys
import os

def main():
    """Launch the Streamlit demo"""
    print("🧬 Starting AlphaGenome Streamlit Demo")
    print("=" * 50)
    
    # Check if streamlit is installed
    try:
        import streamlit
        print("✅ Streamlit found")
    except ImportError:
        print("❌ Streamlit not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
        print("✅ Streamlit installed")
    
    # Check if we have the demo file
    demo_file = "streamlit_alphagenome_demo.py"
    if not os.path.exists(demo_file):
        print(f"❌ Demo file {demo_file} not found")
        return False
    
    print(f"🚀 Launching Streamlit app: {demo_file}")
    print("📱 Your browser should open automatically")
    print("🔗 If not, visit: http://localhost:8501")
    print("⏹️ Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Launch streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", demo_file,
            "--server.address", "localhost",
            "--server.port", "8501",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Streamlit demo stopped")
    except Exception as e:
        print(f"❌ Error launching Streamlit: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 