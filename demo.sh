#!/bin/bash
# Demo script to show the generator in action

echo "================================"
echo "Top10 Generator Demo"
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Install dependencies if needed
echo "Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "Running generator..."
echo ""

# Run the generator
python3 generate.py

echo ""
echo "================================"
echo "Demo complete!"
echo ""
echo "The generated site is available at:"
echo "  output/index.html"
echo ""
echo "Open it in your browser to see the Top 10 deals!"
echo "================================"
