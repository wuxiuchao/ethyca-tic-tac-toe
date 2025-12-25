#!/bin/bash

# Tic-Tac-Toe Server Launcher Script

echo "=== Tic-Tac-Toe Server Launcher ==="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Create logs directory if it doesn't exist
mkdir -p logs

# Start the server
echo ""
echo "Starting Tic-Tac-Toe server..."
echo "Press Ctrl+C to stop the server"
echo ""
python -m app.server

