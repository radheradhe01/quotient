#!/bin/bash

echo "🚀 QUOTIENT BOT - INSTALLATION SCRIPT"
echo "======================================"
echo ""
echo "This script will install and setup Quotient Discord Bot"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+ first."
    echo "   Visit: https://python.org/downloads/"
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python version $python_version is too old. Required: $required_version+"
    exit 1
fi

echo "✅ Python $python_version detected"

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not available. Please install pip first."
    exit 1
fi

echo "✅ pip3 detected"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Run setup script
echo ""
echo "🎯 Running Quotient Bot Setup..."
python setup_quotient.py

echo ""
echo "🎉 Installation completed!"
echo ""
echo "📖 Next steps:"
echo "   1. Read README_SETUP.md for detailed instructions"
echo "   2. Start your bot with: ./start_quotient.sh"
echo "   3. Join our support server for help"
echo ""
echo "🚀 Welcome to Quotient Bot!"

