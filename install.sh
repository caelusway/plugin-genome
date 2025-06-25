#!/bin/bash

# AlphaGenome Installation Script
# Based on official documentation

set -e

echo "🧬 AlphaGenome Installation Script"
echo "=================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python version: $python_version"

# Create virtual environment (recommended by documentation)
echo "📦 Creating virtual environment..."
python3 -m venv alphagenome-env

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source alphagenome-env/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install AlphaGenome using the official method
echo "📦 Installing AlphaGenome..."
pip install -U alphagenome

# Install additional dependencies
echo "📦 Installing additional dependencies..."
pip install -r requirements.txt

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "📋 To use AlphaGenome:"
echo "1. Activate the virtual environment: source alphagenome-env/bin/activate"
echo "2. Set your API key: export ALPHA_GENOME_API_KEY='your-api-key'"
echo "3. Run the setup script: python setup_alphagenome.py"
echo "4. Test basic functionality: python basic_example.py"
echo ""
echo "📚 For more information, check the official documentation:"
echo "   https://www.alphagenomedocs.com/" 