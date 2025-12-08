#!/bin/bash

# Lungs Exposure Risk Visualizer - Quick Start (Linux/macOS)

echo ""
echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║   LUNGS EXPOSURE RISK VISUALIZER - Quick Start (Linux/macOS)    ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "Please install Python 3.8+ using your package manager"
    exit 1
fi

echo "✓ Python detected: $(python3 --version)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

echo ""
echo "🔌 Activating virtual environment..."
source venv/bin/activate

echo ""
echo "📥 Installing dependencies..."
pip install -r requirements.txt -q

echo ""
echo "🔑 Checking for .env file..."
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo ""
    echo "1. Visit: https://openweathermap.org/api"
    echo "2. Create a free account"
    echo "3. Get your API key"
    echo "4. Create a .env file in this directory with:"
    echo ""
    echo "OPENWEATHER_API_KEY=your_api_key_here"
    echo ""
    read -p "Press Enter to continue..."
fi

echo ""
echo "🚀 Starting Flask server..."
echo ""
echo "=========================================="
echo "Opening browser to: http://localhost:5000"
echo "=========================================="
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Open browser (different commands for Linux/macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    open http://localhost:5000
else
    xdg-open http://localhost:5000 2>/dev/null || true
fi

python app.py
