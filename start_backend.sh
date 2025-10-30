#!/bin/bash

echo "🛡️ SHIELD Backend Startup Script"
echo

# Function to check Python version
check_python_version() {
    local python_cmd=$1
    if command -v $python_cmd &> /dev/null; then
        local version=$($python_cmd --version 2>&1 | cut -d' ' -f2)
        local major=$(echo $version | cut -d'.' -f1)
        local minor=$(echo $version | cut -d'.' -f2)
        
        if [ "$major" -ge 3 ] && [ "$minor" -ge 8 ]; then
            echo "✅ Python $version found using $python_cmd"
            PYTHON_CMD=$python_cmd
            return 0
        else
            echo "⚠️ Python $version found but requires 3.8+"
            return 1
        fi
    fi
    return 1
}

# Try to find a suitable Python version
PYTHON_CMD=""

if check_python_version "python3"; then
    :
elif check_python_version "python"; then
    :
elif check_python_version "python3.11"; then
    :
elif check_python_version "python3.10"; then
    :
elif check_python_version "python3.9"; then
    :
elif check_python_version "python3.8"; then
    :
else
    echo "❌ Python 3.8+ is not installed or not in PATH"
    echo "Please install Python 3.8+ from https://python.org"
    echo "On Ubuntu/Debian: sudo apt-get install python3 python3-venv python3-pip"
    echo "On CentOS/RHEL: sudo yum install python3 python3-venv python3-pip"
    echo "On macOS: brew install python3 or install from python.org"
    exit 1
fi

# Navigate to backend directory
cd "$(dirname "$0")/backend" || exit 1

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        echo "On Ubuntu/Debian, you might need: sudo apt-get install python3-venv"
        echo "On CentOS/RHEL, you might need: sudo yum install python3-venv"
        exit 1
    fi
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "❌ Failed to activate virtual environment"
    echo "Trying to recreate virtual environment..."
    rm -rf venv
    $PYTHON_CMD -m venv venv
    source venv/bin/activate
    if [ $? -ne 0 ]; then
        echo "❌ Still failed to activate virtual environment"
        exit 1
    fi
fi

# Upgrade pip first
echo "📦 Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies with better error handling
echo "📦 Installing dependencies..."
python -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install some dependencies"
    echo "Trying to install core dependencies only..."
    python -m pip install "fastapi>=0.95.0,<1.0.0" "uvicorn[standard]>=0.20.0,<1.0.0" "pydantic>=2.0.0,<3.0.0" "pydantic-settings>=2.0.0,<3.0.0" "python-multipart>=0.0.5"
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install core dependencies"
        echo "Please check your internet connection and Python installation"
        exit 1
    fi
    echo "⚠️ Installed core dependencies only. Some features may be limited."
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
    else
        cat > .env << EOF
DEBUG=true
HOST=127.0.0.1
PORT=8000
LOG_LEVEL=INFO
EOF
    fi
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