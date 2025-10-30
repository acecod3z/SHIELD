#!/bin/bash

echo "🛡️ SHIELD Backend Startup Script"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8+ from https://python.org"
    exit 1
fi

echo "✅ Python found"

# Navigate to backend directory
cd "$(dirname "$0")/backend" || exit 1

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
fi

# Start the server
echo
echo "🚀 Starting SHIELD Backend Server..."
echo
echo "The API will be available at:"
echo "  • API: http://127.0.0.1:8000"
echo "  • Docs: http://127.0.0.1:8000/docs"
echo
echo "Press Ctrl+C to stop the server"
echo

python main.py