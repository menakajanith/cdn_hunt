$ErrorActionPreference = "Stop"

# Check if Python3 is installed
if (-not (Get-Command python3 -ErrorAction SilentlyContinue)) {
    Write-Error "Python3 is not installed. Please install Python3 and try again."
    exit 1
}

# Check if pip is installed
if (-not (Get-Command pip3 -ErrorAction SilentlyContinue)) {
    Write-Error "pip3 is not installed. Please install pip3 and try again."
    exit 1
}

# Create project directory
$PROJECT_DIR = "cdn_hunt"
if (-not (Test-Path $PROJECT_DIR)) {
    New-Item -ItemType Directory -Name $PROJECT_DIR
}
Set-Location $PROJECT_DIR

# Download necessary files from GitHub repository
$REPO_URL = "https://raw.githubusercontent.com/menakajanith/cdn_hunt/main"
Invoke-WebRequest -Uri "$REPO_URL/app.py" -OutFile "app.py"
if (-not (Test-Path "templates")) {
    New-Item -ItemType Directory -Name "templates"
}
Invoke-WebRequest -Uri "$REPO_URL/templates/index.html" -OutFile "templates/index.html"

# Create and activate virtual environment
python3 -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install flask requests dnspython ipwhois beautifulsoup4 colorama tqdm

# Run the Flask application
Write-Host "Starting CDN HUNT web application..."
Start-Process python -ArgumentList "app.py" -NoNewWindow

# Wait for the server to start
Start-Sleep -Seconds 5

# Open the web application in the default browser
Start-Process "http://localhost:5000"

Write-Host "CDN HUNT is running at http://localhost:5000"
