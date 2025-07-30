#!/bin/bash

# Exit on any error
set -e

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install Python3 and try again."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is not installed. Please install pip3 and try again."
    exit 1
fi

# Create project directory
PROJECT_DIR="cdn_hunt"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Download necessary files from GitHub repository
REPO_URL="https://raw.githubusercontent.com/menakajanith/cdn_hunt/main"
curl -sL "$REPO_URL/app.py" -o app.py
mkdir -p templates
curl -sL "$REPO_URL/templates/index.html" -o templates/index.html

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install flask requests dnspython ipwhois beautifulsoup4 colorama tqdm

# Run the Flask application
echo "Starting CDN HUNT web application..."
python app.py &

# Wait for the server to start (give it a few seconds)
sleep 5

# Open the web application in the default browser (optional, works on systems with 'xdg-open')
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:5000
fi

echo "CDN HUNT is running at http://localhost:5000"
