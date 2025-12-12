# Resource Planner - Windows Setup Script
# PowerShell script to setup and run the React app on Windows

Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     Epsilon Resource Planner - Windows Setup             ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Function to check if command exists
function Test-Command($cmdname) {
    return [bool](Get-Command -Name $cmdname -ErrorAction SilentlyContinue)
}

# Check prerequisites
Write-Host "🔍 Checking prerequisites..." -ForegroundColor Blue
Write-Host ""

if (-not (Test-Command python)) {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.7+ from https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Yellow
    exit 1
}

if (-not (Test-Command node)) {
    Write-Host "❌ Node.js is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Node.js 16+ from https://nodejs.org/" -ForegroundColor Yellow
    exit 1
}

if (-not (Test-Command npm)) {
    Write-Host "❌ npm is not installed" -ForegroundColor Red
    Write-Host "npm should come with Node.js. Please reinstall Node.js" -ForegroundColor Yellow
    exit 1
}

$pythonVersion = python --version
$nodeVersion = node --version
$npmVersion = npm --version

Write-Host "✅ $pythonVersion" -ForegroundColor Green
Write-Host "✅ Node.js $nodeVersion" -ForegroundColor Green
Write-Host "✅ npm $npmVersion" -ForegroundColor Green
Write-Host ""

# Setup backend
Write-Host "📦 Setting up backend..." -ForegroundColor Blue
Set-Location backend

Write-Host "Installing Python dependencies..." -ForegroundColor Cyan
pip install flask flask-cors

if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Warning: pip install had issues. Trying alternative method..." -ForegroundColor Yellow
    python -m pip install flask flask-cors
}

Write-Host "✅ Backend setup complete!" -ForegroundColor Green
Write-Host ""

# Setup frontend
Write-Host "📦 Setting up frontend..." -ForegroundColor Blue
Set-Location ..\frontend

if (-not (Test-Path "node_modules")) {
    Write-Host "Installing Node.js dependencies..." -ForegroundColor Cyan
    npm install
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ npm install failed" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Dependencies already installed." -ForegroundColor Green
}

Write-Host "✅ Frontend setup complete!" -ForegroundColor Green
Write-Host ""

# Start services
Write-Host "🚀 Starting services..." -ForegroundColor Blue
Write-Host ""

# Start backend in new window
Write-Host "Starting backend server on http://localhost:5000" -ForegroundColor Green
Set-Location ..\backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python backend.py"

# Wait for backend to start
Start-Sleep -Seconds 3

# Start frontend
Set-Location ..\frontend
Write-Host "Starting frontend server on http://localhost:3000" -ForegroundColor Green
Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                     🎉 Ready to Go!                      ║" -ForegroundColor Cyan
Write-Host "║                                                           ║" -ForegroundColor Cyan
Write-Host "║  Backend:  http://localhost:5000                         ║" -ForegroundColor Cyan
Write-Host "║  Frontend: http://localhost:3000                         ║" -ForegroundColor Cyan
Write-Host "║                                                           ║" -ForegroundColor Cyan
Write-Host "║  Press Ctrl+C in this window to stop frontend            ║" -ForegroundColor Cyan
Write-Host "║  Close the Python window to stop backend                 ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

npm run dev
